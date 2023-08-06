"""
Functions to fit automatic-differentiable models to aerodynamic data from an airfoil.
Requires the xfoil package from PyPI; see aerosandbox.geometry for more information on this.
"""
from aerosandbox.geometry import *
from aerosandbox.tools.fitting import *
from aerosandbox.tools.miscellaneous import eng_string, remove_nans
import plotly.express as px
import plotly.graph_objects as go
import dill as pickle
import multiprocessing_on_dill as mp
import time


class AirfoilFitter():
    def __init__(self,
                 airfoil,  # type: Airfoil
                 parallel = True,
                 ):
        airfoil.has_xfoil_data()
        self.airfoil = airfoil

    def plot_xfoil_alpha_Re(self,
                            y_data_name,
                            model=None,
                            params_solved=None,
                            title=None,
                            log_z=False,
                            show=True
                            ):
        """
        See the docstring of the "fit" function in aerosandbox.tools.casadi_tools for syntax.
        :param model:
        :param x_data:
        :param y_data:
        :param params_solved:
        :param title:
        :param show:
        :return:
        """
        # Make plot
        fig = go.Figure()
        fig.add_trace(
            go.Scatter3d(
                x=self.airfoil.xfoil_data_1D['alpha'],
                y=self.airfoil.xfoil_data_1D['Re'],
                z=self.airfoil.xfoil_data_1D[y_data_name],
                mode="markers",
                marker=dict(
                    size=2,
                    color="black"
                )
            )
        )
        if model is not None:
            # Get model data
            n = 60
            linspace = lambda x: np.linspace(np.min(x), np.max(x), n)
            logspace = lambda x: np.logspace(np.log10(np.min(x)), np.log10(np.max(x)), n)
            x1 = linspace(self.airfoil.xfoil_data_1D['alpha'])
            x2 = logspace(self.airfoil.xfoil_data_1D['Re'])
            X1, X2 = np.meshgrid(x1, x2)
            x_model = {
                'alpha': X1.reshape(-1),
                'Re'   : X2.reshape(-1)
            }
            y_model = np.array(model(x_model, params_solved)).reshape((n, n))
            fig.add_trace(
                go.Surface(
                    contours={
                        # "x": {"show": True, "start": -20, "end": 20, "size": 1},
                        # "y": {"show": True, "start": 1e4, "end": 1e6, "size": 1e5},
                        # "z": {"show": True, "start": -5, "end": 5, "size": 0.1}
                    },
                    x=x1,
                    y=x2,
                    z=y_model,
                    # intensity=y_model,
                    colorscale="plasma",
                    # flatshading=True
                )
            )
        fig.update_layout(
            scene=dict(
                xaxis=dict(
                    title="Alpha"
                ),
                yaxis=dict(
                    type='log',
                    title="Re"
                ),
                zaxis=dict(
                    type='log' if log_z else 'linear',
                    title="f(alpha, Re)"
                ),
            ),
            title=title
        )
        if show:
            fig.show()
        return fig

    def fit_xfoil_data_Cl(self,
                          supercritical_Re_threshold=1e6,
                          subcritical_Re_threshold=1e4,
                          plot_fit=True
                          ):

        ### Fit utilities, data extraction, plotting tools
        d = self.airfoil.xfoil_data_1D  # data
        raw_sigmoid = lambda x: x / (1 + x ** 4) ** (1 / 4)

        def sigmoid(
                x, x_cent, x_scale, y_cent, y_scale,
                raw_sigmoid=raw_sigmoid,
        ):
            return y_cent + y_scale * raw_sigmoid((x - x_cent) / x_scale)

        ### Fit the supercritical data
        def model_Cl_turbulent(
                x, p,
                sigmoid=sigmoid,  # packaging dependencies
        ):
            log10_Re = cas.log10(x['Re'])
            Cl_turbulent = (
                    sigmoid(x['alpha'], p['clt_a_c'], p['clt_a_s'], p['clt_cl_c'], p['clt_cl_s']) +
                    p['clt_clre'] * log10_Re
            )
            return Cl_turbulent

        Cl_turbulent_params_guess = {
            'clt_a_c' : 0,
            'clt_a_s' : 12,
            'clt_cl_c': 0,
            'clt_cl_s': 1.5,
            'clt_clre': 0,
        }
        Cl_turbulent_param_bounds = {
            'clt_a_c' : (None, None),
            'clt_a_s' : (0, None),
            'clt_cl_c': (None, None),
            'clt_cl_s': (0, 4),
            'clt_clre': (None, None),
        }

        Cl_turbulent_params_solved = fit(
            model=model_Cl_turbulent,
            x_data=d,
            y_data=d['Cl'],
            param_guesses=Cl_turbulent_params_guess,
            param_bounds=Cl_turbulent_param_bounds,
            weights=np.logical_and(d['Re'] >= supercritical_Re_threshold, True).astype('int')
        )

        # self.plot_xfoil_alpha_Re(
        #     y_data_name='Cl',
        #     model=model_Cl_turbulent,
        #     params_solved=Cl_turbulent_params_solved,
        #     title="Fit: Lift Coefficient (Turbulent)"
        # )

        ### Fit the subcritical data
        def model_Cl_laminar(
                x, p,
                sigmoid=sigmoid,  # packaging dependencies
        ):
            Cl_laminar = (
                    p['cll_cla'] * x['alpha'] + p['cll_cl0'] +
                    sigmoid(x['alpha'], p['clld_a_c'], p['clld_a_s'], 0, p['clld_cl_s'])
            )
            return Cl_laminar

        Cl_laminar_params_guess = {
            'cll_cla'  : 0.04,
            'cll_cl0'  : 0,
            'clld_a_c' : 0,
            'clld_a_s' : 2,
            'clld_cl_s': 0.1,
        }
        Cl_laminar_param_bounds = {
            'cll_cla'  : (0.01, 0.2),
            'cll_cl0'  : (None, 1.5),
            'clld_a_c' : (-8, 8),
            'clld_a_s' : (0, 8),
            'clld_cl_s': (0, 0.4),
        }

        Cl_laminar_params_solved = fit(
            model=model_Cl_laminar,
            x_data=d,
            y_data=d['Cl'],
            param_guesses=Cl_laminar_params_guess,
            param_bounds=Cl_laminar_param_bounds,
            weights=np.logical_and(d['Re'] <= subcritical_Re_threshold, True).astype('int')
        )

        # self.plot_xfoil_alpha_Re(
        #     y_data_name='Cl',
        #     model=model_Cl_laminar,
        #     params_solved=Cl_laminar_params_solved,
        #     title="Fit: Lift Coefficient (Laminar)"
        # )

        # Fit the blend
        def model_Cl_blend(
                x, p,
                sigmoid=sigmoid,  # packaging dependencies
                model_Cl_turbulent=model_Cl_turbulent,  # packaging dependencies
                model_Cl_laminar=model_Cl_laminar,  # packaging dependencies
        ):
            v = lambda x, k, a: (k + x ** 2) ** 0.5 + a * x

            log10_Re = cas.log10(x['Re'])
            blend_input = -p['clb_hardness'] * (
                    p['clb_a_scale'] * v(x['alpha'] - p['clb_a_0'], 0.1, p['clb_asym']) + p['clb_re_0']
                    - log10_Re
            )
            blend = sigmoid(blend_input, 0, 1, 0.5, 0.5)
            Cl = blend * model_Cl_turbulent(x, p) + (1 - blend) * model_Cl_laminar(x, p)
            return Cl

        Cl_blend_params_guess = {
            **Cl_turbulent_params_solved,
            **Cl_laminar_params_solved,
            'clb_hardness': 1.7,
            'clb_a_scale' : 0.3,
            'clb_asym'    : 0.5,
            'clb_a_0'     : 6,
            'clb_re_0'    : 3.5,

        }
        Cl_blend_param_bounds = {
            'clb_hardness': (1e-3, 10),
            'clb_a_scale' : (0, 1),
            'clb_a_0'     : (-4, 12),
            'clb_re_0'    : (3, 6),
        }

        Cl_blend_params_solved = fit(
            model=model_Cl_blend,
            x_data=d,
            y_data=d['Cl'],
            param_guesses=Cl_blend_params_guess,
            param_bounds={
                # **{k: (v, v) for k, v in Cl_laminar_params_solved.items()},
                # **{k: (v, v) for k, v in Cl_turbulent_params_solved.items()},
                **Cl_laminar_param_bounds,
                **Cl_turbulent_param_bounds,
                **Cl_blend_param_bounds
            },
            # weights=(d['Cl'] >= 0).astype('int')
        )

        if plot_fit:
            self.plot_xfoil_alpha_Re(
                y_data_name='Cl',
                model=model_Cl_blend,
                params_solved=Cl_blend_params_solved,
                title="Fit: Lift Coefficient (Blend)"
            )

        # Make the final function.
        def Cl_function(
                alpha, Re,
                Cl_blend_params_solved=Cl_blend_params_solved,  # packaging dependencies
                model_Cl_blend=model_Cl_blend  # packaging dependencies
        ):
            return model_Cl_blend(
                x={'alpha': alpha, 'Re': Re},
                p=Cl_blend_params_solved
            )

        self.Cl_function = Cl_function
        return Cl_function

    def fit_xfoil_data_Cd(self,
                          supercritical_Re_threshold=1e6,
                          subcritical_Re_threshold=1e4,
                          plot_fit=True
                          ):

        ### Fit utilities, data extraction, plotting tools
        d = self.xfoil_data_1D  # data
        raw_sigmoid = lambda x: x / (1 + x ** 4) ** (1 / 4)
        sigmoid = lambda x, x_cent, x_scale, y_cent, y_scale: y_cent + y_scale * raw_sigmoid((x - x_cent) / x_scale)

        ### Fit the supercritical data
        def model_log10_Cd_turbulent(x, p):
            a = x['alpha']
            log10_Re = cas.log10(x['Re'])
            log10_Cd_turbulent = (
                    p['cdt_0'] +
                    p['cdt_a1'] * a +
                    p['cdt_Re1'] * log10_Re +
                    p['cdt_a2'] * a ** 2 +
                    p['cdt_aRe'] * a * log10_Re +
                    p['cdt_Re2'] * log10_Re ** 2
            )

            return log10_Cd_turbulent

        model_Cd_turbulent = lambda *args: 10 ** model_log10_Cd_turbulent(*args)

        log10_Cd_turbulent_params_guess = {
            'cdt_0'  : -2,
            'cdt_a1' : 0,
            'cdt_Re1': -1,
            'cdt_a2' : 0.0035,
            'cdt_aRe': 0,
            'cdt_Re2': 0.01,
        }
        log10_Cd_turbulent_param_bounds = {
        }

        Cd_turbulent_params_solved = fit(
            model=model_log10_Cd_turbulent,
            x_data=d,
            y_data=cas.log10(d['Cd']),
            param_guesses=log10_Cd_turbulent_params_guess,
            param_bounds=log10_Cd_turbulent_param_bounds,
            weights=np.logical_and(d['Re'] >= supercritical_Re_threshold, True).astype('int')
        )

        self.plot_xfoil_alpha_Re(
            y_data_name='Cd',
            model=model_Cd_turbulent,
            params_solved=Cd_turbulent_params_solved,
            title="Fit: Lift Coefficient (Turbulent)",
            log_z=True
        )

        # ### Fit the subcritical data
        # def model_Cd_laminar(x, p):
        #     Cd_laminar = (
        #             p['cdl_cda'] * x['alpha'] + p['cdl_cd0'] +
        #             sigmoid(x['alpha'], p['cdld_a_c'], p['cdld_a_s'], 0, p['cdld_cd_s'])
        #     )
        #     return Cd_laminar
        #
        # Cd_laminar_params_guess = {
        #     'cdl_cda'  : 0.04,
        #     'cdl_cd0'  : 0,
        #     'cdld_a_c' : 0,
        #     'cdld_a_s' : 2,
        #     'cdld_cd_s': 0.1,
        # }
        # Cd_laminar_param_bounds = {
        #     'cdl_cda'  : (0.01, 0.2),
        #     'cdl_cd0'  : (None, 1.5),
        #     'cdld_a_c' : (-8, 8),
        #     'cdld_a_s' : (0, 8),
        #     'cdld_cd_s': (0, 0.4),
        # }
        #
        # Cd_laminar_params_solved = fit(
        #     model=model_Cd_laminar,
        #     x_data=d,
        #     y_data=d['Cd'],
        #     param_guesses=Cd_laminar_params_guess,
        #     param_bounds=Cd_laminar_param_bounds,
        #     weights=np.logical_and(d['Re'] <= subcritical_Re_threshold, True).astype('int')
        # )
        #
        # # self.plot_xfoil_alpha_Re(
        # #     y_data_name='Cd',
        # #     model=model_Cd_laminar,
        # #     params_solved=Cd_laminar_params_solved,
        # #     title="Fit: Lift Coefficient (Laminar)"
        # # )
        #
        # # Fit the blend
        # def model_Cd_blend(x, p):
        #     v = lambda x, k, a: (k + x ** 2) ** 0.5 + a * x
        #
        #     log10_Re = cas.log10(x['Re'])
        #     blend_input = -p['cdb_hardness'] * (
        #             p['cdb_a_scale'] * v(x['alpha'] - p['cdb_a_0'], 0.1, p['cdb_asym']) + p['cdb_re_0']
        #             - log10_Re
        #     )
        #     blend = sigmoid(blend_input, 0, 1, 0.5, 0.5)
        #     Cd = blend * model_Cd_turbulent(x, p) + (1 - blend) * model_Cd_laminar(x, p)
        #     return Cd
        #
        # Cd_blend_params_guess = {
        #     **Cd_turbulent_params_solved,
        #     **Cd_laminar_params_solved,
        #     'cdb_hardness': 1.7,
        #     'cdb_a_scale' : 0.3,
        #     'cdb_asym'    : 0.5,
        #     'cdb_a_0'     : 6,
        #     'cdb_re_0'    : 3.5,
        #
        # }
        # Cd_blend_param_bounds = {
        #     'cdb_hardness': (1e-3, 10),
        #     'cdb_a_scale' : (0, 1),
        #     'cdb_a_0'     : (-4, 12),
        #     'cdb_re_0'    : (3, 6),
        # }
        #
        # Cd_blend_params_solved = fit(
        #     model=model_Cd_blend,
        #     x_data=d,
        #     y_data=d['Cd'],
        #     param_guesses=Cd_blend_params_guess,
        #     param_bounds={
        #         # **{k: (v, v) for k, v in Cd_laminar_params_solved.items()},
        #         # **{k: (v, v) for k, v in Cd_turbulent_params_solved.items()},
        #         **Cd_laminar_param_bounds,
        #         **Cd_turbulent_param_bounds,
        #         **Cd_blend_param_bounds
        #     },
        #     # weights=(d['Cd'] >= 0).astype('int')
        # )
        #
        # if plot_fit:
        #     self.plot_xfoil_alpha_Re(
        #         y_data_name='Cd',
        #         model=model_Cd_blend,
        #         params_solved=Cd_blend_params_solved,
        #         title="Fit: Lift Coefficient (Blend)"
        #     )
        #
        # # Make the final function, packaging parameters using an inner function.
        # def outer(
        #         Cd_blend_params_solved
        # ):
        #     def inner(alpha, Re):
        #         raw_sigmoid = lambda x: x / (1 + x ** 4) ** (1 / 4)
        #         sigmoid = lambda x, x_cent, x_scale, y_cent, y_scale: y_cent + y_scale * raw_sigmoid(
        #             (x - x_cent) / x_scale)
        #
        #         def model_Cd_turbulent(x, p):
        #             log10_Re = cas.log10(x['Re'])
        #             Cd_turbulent = (
        #                     sigmoid(x['alpha'], p['cdt_a_c'], p['cdt_a_s'], p['cdt_cd_c'], p['cdt_cd_s']) +
        #                     p['cdt_cdre'] * log10_Re
        #             )
        #             return Cd_turbulent
        #
        #         def model_Cd_laminar(x, p):
        #             Cd_laminar = (
        #                     p['cdl_cda'] * x['alpha'] + p['cdl_cd0'] +
        #                     sigmoid(x['alpha'], p['cdld_a_c'], p['cdld_a_s'], 0, p['cdld_cd_s'])
        #             )
        #             return Cd_laminar
        #
        #         def model_Cd_blend(x, p):
        #             v = lambda x, k, a: (k + x ** 2) ** 0.5 + a * x
        #
        #             log10_Re = cas.log10(x['Re'])
        #             blend_input = -p['cdb_hardness'] * (
        #                     p['cdb_a_scale'] * v(x['alpha'] - p['cdb_a_0'], 0.1, p['cdb_asym']) + p['cdb_re_0']
        #                     - log10_Re
        #             )
        #             blend = sigmoid(blend_input, 0, 1, 0.5, 0.5)
        #             Cd = blend * model_Cd_turbulent(x, p) + (1 - blend) * model_Cd_laminar(x, p)
        #             return Cd
        #
        #         return model_Cd_blend(
        #             x={'alpha': alpha, 'Re': Re},
        #             p=Cd_blend_params_solved
        #         )
        #
        #     return inner
        #
        # Cd_function = outer(
        #     Cd_blend_params_solved
        # )
        #
        # self.Cd_function = Cd_function
        # return Cd_function

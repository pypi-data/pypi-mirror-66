def data(casings=[], d_openhole=0.216):
    from numpy import asarray
    dict = {'tin': 20.0, 'ts': 15.0, 'wd': 100.0,  'ddi': 4.0, 'ddo': 4.5, 'dri': 17.716, 'dro': 21.0, 'dfm': 80.0,
            'q': 794.933, 'lambdal': 0.635, 'lambdac': 43.3, 'lambdacem': 0.7, 'lambdad': 40.0, 'lambdafm': 2.249,
            'lambdar': 15.49, 'lambdaw': 0.6, 'cl': 3713.0, 'cc': 469.0, 'ccem': 2000.0, 'cd': 400.0, 'cr': 464.0,
            'cw': 4000.0, 'cfm': 800.0, 'rhof': 1.198, 'rhod': 7.8, 'rhoc': 7.8, 'rhor': 7.8, 'rhofm': 2.245,
            'rhow': 1.029, 'rhocem': 2.7, 'gt': 0.0238, 'wtg': -0.005, 'rpm': 100.0, 'tbit': 9, 'wob': 50, 'rop': 30.4,
            'an': 3100.0, 'bit_n': 1.0, 'dp_e': 0.0, 'thao_o': 1.82, 'beta': 44983 * 10 ** 5, 'alpha': 960 * 10 ** -6,
            'k': 0.3832, 'n': 0.7, 'visc': 0}

    if len(casings) > 0:
        od = sorted([x['od'] * 0.0254 for x in casings])
        id = sorted([x['id'] * 0.0254 for x in casings])
        depth = sorted([x['depth'] for x in casings], reverse=True)
        dict['casings'] = [[od[x], id[x], depth[x]] for x in range(len(casings))]
        dict['casings'] = asarray(dict['casings'])
    else:
        dict['casings'] = [[(d_openhole + dict['dro'] * 0.0254), d_openhole, 0]]
        dict['casings'] = asarray(dict['casings'])

    return dict


def info(about='all'):
    print("Use the ID of a parameter to change the default value (e.g. tdict['tin']=30 to change the fluid inlet "
          "temperature from the default value to 30° Celsius)")
    print('Notice that the information is provided as follows:' + '\n' +
          'parameter ID: general description, units' + '\n')

    tubular_parameters = 'VALUES RELATED TO TUBULAR SIZES' + '\n' + \
                         'ddi: drill string inner diameter, in' + '\n' + \
                         'ddo: drill string outer diameter, in' + '\n' + \
                         'dri: riser inner diameter, in' + '\n' + \
                         'dro: riser outer diameter, in' + '\n'

    conditions_parameters = 'PARAMETERS RELATED TO SIMULATION CONDITIONS' + '\n' + \
                            'ts: surface temperature, °C' + '\n' + \
                            'wd: water depth, m' + '\n' + \
                            'dfm: undisturbed formation diameter, m' + '\n'

    heatcoeff_parameters = 'PARAMETERS RELATED TO HEAT COEFFICIENTS' + '\n' + \
                           'lambdal: fluid - thermal conductivity, W/(m*°C)' + '\n' + \
                           'lambdac: casing - thermal conductivity, W/(m*°C)' + '\n' + \
                           'lambdacem: cement - thermal conductivity, W/(m*°C)' + '\n' + \
                           'lambdad: drill pipe - thermal conductivity, W/(m*°C)' + '\n' + \
                           'lambdafm: formation - thermal conductivity, W/(m*°C)' + '\n' + \
                           'lambdar: riser - thermal conductivity, W/(m*°C)' + '\n' + \
                           'lambdaw: water - thermal conductivity, W/(m*°C)' + '\n' + \
                           'cl: fluid - specific heat capacity, J/(kg*°C)' + '\n' + \
                           'cc: casing - specific heat capacity, J/(kg*°C)' + '\n' + \
                           'ccem: cement - specific heat capacity, J/(kg*°C)' + '\n' + \
                           'cd: drill pipe - specific heat capacity, J/(kg*°C)' + '\n' + \
                           'cr: riser - specific heat capacity, J/(kg*°C)' + '\n' + \
                           'cw: water - specific heat capacity, J/(kg*°C)' + '\n' + \
                           'cfm: formation - specific heat capacity, J/(kg*°C)' + '\n' + \
                           'gt: geothermal gradient, °C/m' + '\n' + \
                           'wtg: seawater thermal gradient, °C/m' + '\n'

    densities_parameters = 'PARAMETERS RELATED TO DENSITIES' + '\n' + \
                           'rhof: fluid density, sg' + '\n' + \
                           'rhod: drill pipe density, sg' + '\n' + \
                           'rhoc: casing density, sg' + '\n' + \
                           'rhor: riser density, sg' + '\n' + \
                           'rhofm: formation density, sg' + '\n' + \
                           'rhow: seawater density, sg' + '\n' + \
                           'rhocem: cement density, sg' + '\n' + \
                           'beta: isothermal bulk modulus, Pa' + '\n' + \
                           'alpha: expansion coefficient, 1/°C' + '\n'

    viscosity_parameters = 'PARAMETERS RELATED TO MUD VISCOSITY' + '\n' + \
                           'thao_o: yield stress, Pa' + '\n' + \
                           'n: flow behavior index, dimensionless' + '\n' + \
                           'k: consistency index, Pa*s^n' + '\n' + \
                           'visc: fluid viscosity, cp' + '\n'

    operational_parameters = 'PARAMETERS RELATED TO THE OPERATION' + '\n' + \
                             'tin: fluid inlet temperature, °C' + '\n' + \
                             'q: flow rate, lpm' + '\n' + \
                             'rpm: revolutions per minute' + '\n' + \
                             'tbit: torque on the bit, kN*m' + '\n' + \
                             'wob: weight on bit, kN' + '\n' + \
                             'rop: rate of penetration, m/h' + '\n' + \
                             'an: area of the nozzles, in^2' + '\n' + \
                             'bit_n: drill bit efficiency' + '\n' + \
                             'dp_e: drill pipe eccentricity' + '\n'

    if about == 'casings':
        print(tubular_parameters)

    if about == 'conditions':
        print(conditions_parameters)

    if about == 'heatcoeff':
        print(heatcoeff_parameters)

    if about == 'densities':
        print(densities_parameters)

    if about == 'operational':
        print(operational_parameters)

    if about == 'viscosity':
        print(viscosity_parameters)

    if about == 'all':
        print(tubular_parameters + '\n' + conditions_parameters + '\n' + heatcoeff_parameters + '\n' +
              densities_parameters + '\n' + viscosity_parameters + '\n' + operational_parameters)


def set_well(temp_dict, depths, visc_eq=True):
    from math import pi, log

    class NewWell(object):
        def __init__(self):
            # DEPTH
            self.md = depths.md
            self.tvd = depths.tvd
            self.deltaz = depths.deltaz
            self.zstep = depths.zstep
            self.sections = depths.sections
            self.north = depths.north
            self.east = depths.east
            self.inclination = depths.inclination
            self.dogleg = depths.dogleg
            self.azimuth = depths.azimuth

            # TUBULAR
            self.casings = temp_dict["casings"]  # casings array
            self.riser = round(temp_dict["wd"] / self.deltaz)  # number of grid cells for the riser
            self.ddi = temp_dict["ddi"] * 0.0254  # Drill String Inner  Diameter, m
            self.ddo = temp_dict["ddo"] * 0.0254   # Drill String Outer Diameter, m
            self.dri = temp_dict["dri"] * 0.0254  # Riser diameter Inner Diameter, m
            self.dro = temp_dict["dro"] * 0.0254   # Riser diameter Outer Diameter, m

            # CONDITIONS
            self.ts = temp_dict["ts"]  # Surface Temperature (RKB), °C
            self.wd = temp_dict["wd"]  # Water Depth, m
            self.dsr = self.casings[0, 0]  # Surrounding Space Inner Diameter, m
            self.dsro = sorted([self.dro + 0.03, self.casings[-1, 0] + 0.03])[-1]  # Surrounding Space Outer Diameter, m
            self.dfm = temp_dict["dfm"]  # Undisturbed Formation Diameter, m

            # RADIUS (CALCULATED)
            self.r1 = self.ddi / 2  # Drill String Inner  Radius, m
            self.r2 = self.ddo / 2  # Drill String Outer Radius, m
            self.r3 = self.casings[0, 1] / 2  # Casing Inner Radius, m
            self.r3r = self.dri / 2  # Riser Inner Radius, m
            self.r4r = self.dro / 2  # Riser Outer Radius, m
            self.r4 = self.casings[0, 0] / 2  # Surrounding Space Inner Radius m
            self.r5 = self.dsro / 2  # Surrounding Space Outer Radius, m
            self.rfm = self.dfm / 2  # Undisturbed Formation Radius, m

            # DENSITIES kg/m3
            self.rhof = temp_dict["rhof"] * 1000  # Fluid
            self.rhod = temp_dict["rhod"] * 1000  # Drill Pipe
            self.rhoc = temp_dict["rhoc"] * 1000  # Casing
            self.rhor = temp_dict["rhor"] * 1000  # Riser
            self.rhocem = temp_dict["rhocem"] * 1000  # Cement Sheath
            self.rhofm = temp_dict["rhofm"] * 1000  # Formation
            self.rhow = temp_dict["rhow"] * 1000  # Seawater

            # OPERATIONAL
            self.tin = temp_dict["tin"]  # Inlet Fluid temperature, °C
            self.q = temp_dict["q"] * 0.06  # Flow rate, m^3/h
            self.va = (self.q / (pi * ((self.r3 ** 2) - (self.r2 ** 2)))) / 3600  # Fluid velocity through the annular
            self.vp = (self.q / (pi * (self.r1 ** 2))) / 3600  # Fluid velocity through the drill pipe
            self.rpm = temp_dict["rpm"]  # Revolutions per minute
            self.tbit = temp_dict["tbit"] # Torque on the bit, kN*m
            self.wob = temp_dict["wob"]  # Weight on bit, kN
            self.rop = temp_dict["rop"]  # Rate of Penetration, m/h
            self.an = temp_dict["an"] / 1550  # Area of the nozzles, m^2
            self.bit_n = temp_dict["bit_n"]  # drill bit efficiency
            self.dp_e = temp_dict["dp_e"]  # drill pipe eccentricity

            self.thao_o = temp_dict["thao_o"]
            self.k = temp_dict["k"]
            self.n = temp_dict["n"]

            if temp_dict["visc"] == 0:
                n = self.n
                thao_w = ((self.q / (pi * n * (self.r3 - self.r2) ** 2 * (1 / (2 * (2 * n + 1) * self.k ** (1 / n))) *
                          (self.r3 + self.r2))) + (self.thao_o * (2 * n + 1) / (n + 1)) ** (1 / n)) ** n
                shear_rate = ((thao_w - self.thao_o) / self.k) ** (1/n)
                self.visc_a = (self.thao_o / shear_rate) + self.k * shear_rate ** (n - 1)  # Fluid viscosity [Pas]

                if visc_eq:
                    self.visc_p = self.visc_a
                else:
                    from sympy import symbols, solve
                    x = symbols('x')
                    expr = self.q - (pi * n * self.r1 ** 3 * (1 / (3 * n + 1)) * (x / self.k) ** (1 / n) * (1 -
                            (3 * n + 1) * (self.thao_o) / (n * (2 * n + 1) * x)))
                    sol = solve(expr)
                    thao_w_p = sol[0]
                    shear_rate_p = ((thao_w_p - self.thao_o) / self.k) ** (1 / n)
                    self.visc_p = float((self.thao_o / shear_rate_p) + self.k * shear_rate_p ** (n - 1))

            else:
                self.visc_p = self.visc_a = temp_dict["visc"] / 1000

            # HEAT COEFFICIENTS
            self.lambdal = temp_dict["lambdal"]  # Fluid
            self.lambdac = temp_dict["lambdac"]  # Casing
            self.lambdacem = temp_dict["lambdacem"]  # Cement
            self.lambdad = temp_dict["lambdad"]  # Drill Pipe
            self.lambdafm = temp_dict["lambdafm"]       # Formation
            self.lambdar = temp_dict["lambdar"]     # Riser
            self.lambdaw = temp_dict["lambdaw"]     # Seawater
            self.beta = temp_dict["beta"]  # Fluid Thermal Expansion Coefficient
            self.alpha = temp_dict['alpha']
            self.cl = temp_dict["cl"]       # Fluid
            self.cc = temp_dict["cc"]    # Casing
            self.ccem = temp_dict["ccem"]     # Cement
            self.cd = temp_dict["cd"]     # Drill Pipe
            self.cr = temp_dict["cr"]     # Riser
            self.cw = temp_dict["cw"]      # Seawater
            self.cfm = temp_dict["cfm"]       # Formation
            self.pr_p = self.visc_p * self.cl / self.lambdal       # Prandtl number
            self.pr_a = self.visc_a * self.cl / self.lambdal  # Prandtl number
            self.gt = temp_dict["gt"] * self.deltaz  # Geothermal gradient, °C/m
            self.wtg = temp_dict["wtg"] * self.deltaz  # Seawater thermal gradient, °C/m


            # Raise Errors:
            if self.casings[-1, 0] > self.dsro:
                raise ValueError('Last casing outer diameter must be smaller than the surrounding space diameter.')

            if self.casings[0, 2] > self.md[-1]:
                raise ValueError('MD must be higher than the first casing depth.')

            if self.casings[0, 1] < self.ddo:
                raise ValueError('Drill Pipe outer diameter must be smaller than the first casing inner diameter.')

            if self.wd > 0 and self.dro > self.dsro:
                raise ValueError('Riser diameter must be smaller than the surrounding space diameter.')

            if self.dsro > self.dfm:
                raise ValueError('Surrounding space diameter must be smaller than the undisturbed formation diameter.')

        def plot_torque_drag(self, plot='torque'):
            from .plot import plot_torque_drag
            plot_torque_drag(self, plot)

        def wellpath(self):
            return depths

        def define_density(self, ic, cond=0):
            from .fluid import initial_density, calc_density
            from .torque_drag import calc_torque_drag
            if cond == 0:
                self.rhof, self.rhof_initial = initial_density(self, ic)
            else:
                self.rhof = calc_density(self, ic, self.rhof_initial)
            self.drag, self.torque = calc_torque_drag(self)  # Torque/Forces, kN*m / kN
            self.re_p = [x * self.vp * 2 * self.r1 / self.visc_p for x in self.rhof]  # Reynolds number inside drill pipe
            self.re_a = [x * self.va * 2 * (self.r3 - self.r2) / self.visc_a for x in
                         self.rhof]  # Reynolds number - annular
            self.f_p = [1.63 / log(6.9 / x) ** 2 for x in self.re_p]  # Friction factor inside drill pipe
            self.nu_dpi = [0.027 * (x ** (4 / 5)) * (self.pr_p ** (1 / 3)) * (1 ** 0.14) for x in self.re_p]
            self.nu_dpo = [0.027 * (x ** (4 / 5)) * (self.pr_a ** (1 / 3)) * (1 ** 0.14) for x in self.re_a]
            self.h1 = [self.lambdal * x / self.ddi for x in self.nu_dpi]  # Drill Pipe inner wall
            self.h2 = [self.lambdal * x / self.ddo for x in self.nu_dpo]  # Drill Pipe outer wall
            self.nu_a = [1.86 * ((x * self.pr_a) ** (1 / 3)) * ((2 * (self.r3 - self.r2) / self.md[-1]) ** (1 / 3))
                         * (1 ** (1 / 4)) for x in self.re_a]
            # convective heat transfer coefficients, W/(m^2*°C)
            self.h3 = [self.lambdal * x / (2 * self.r3) for x in self.nu_a]  # Casing inner wall
            self.h3r = [self.lambdal * x / (2 * self.r3r) for x in self.nu_a]  # Riser inner wall
            return self

    return NewWell()

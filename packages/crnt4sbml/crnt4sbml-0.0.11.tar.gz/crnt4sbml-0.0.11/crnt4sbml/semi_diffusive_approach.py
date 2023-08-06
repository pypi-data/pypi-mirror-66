
import os
import numpy
import sympy
import sympy.utilities.lambdify
import sys
import numpy.linalg
from .bistability_finder import BistabilityFinder


class SemiDiffusiveApproach:
    """
    Class for constructing variables and methods needed for the semi-diffusive approach.
    """

    def __init__(self, cgraph, get_physiological_range):
        """
        Initialization of the SemiDiffusiveApproach class.

        See also
        ---------
        crnt4sbml.CRNT.get_semi_diffusive_approach()
        """
        self.__cgraph = cgraph
        self.get_physiological_range = get_physiological_range

        self.__g = self.__cgraph.get_graph()
        self.__important_info = ""

        # getting edges and nodes in the order they were added
        self.__g_nodes = self.__cgraph.get_g_nodes()
        self.__g_edges = self.__cgraph.get_g_edges()

        # vars used frequently
        self.__numpy_dtype = None
        self.__N = len(self.__cgraph.get_species())
        self.__R = len(self.__cgraph.get_reactions())
        self.__species = self.__cgraph.get_species()
        self.__reactions = self.__cgraph.get_reactions()
        self.__delta = self.__cgraph.get_deficiency()
        self.__M = len(self.__cgraph.get_complexes())
        self.__my_rank = None
        self.__comm = None
        self.__num_cores = None

        self.__var_nothing_index = [self.__g.nodes[n]['label'] for n in self.__g_nodes if
                                    self.__g.nodes[n]['species_bc']]

        if not self.__var_nothing_index:
            raise Exception("A boundary species is not present, semi-diffusive approach cannot be ran!")

        if not self.__cgraph.get_dim_equilibrium_manifold() == 0:
            print("Conservation laws present.")
            print("The semi-diffusive approach cannot be ran!")
            sys.exit()

        # compute necessary matrices
        self.__create_y_r_matrix()
        self.__create_s_to_matrix()

        self.__find_key_species_indices()
        self.__find_non_key_species_indices()
        self.__create_symbolic_jacobian_matrix()
        self.__create_lambda_jacobian_matrix()
        self.__create_symbolic_objective_function()
        self.__create_lambda_objective_function()
        self.__create_symbolic_polynomial_function()
        self.__create_lambda_polynomial_function()
        self.__create_concentration_pars()
        self.__create_decision_vector()
        self.__create_lambda_equality_poly_fun()

    def get_optimization_bounds(self):
        """
        Returns a list of tuples defining the upper and lower bounds for the decision vector variables based on
        physiological ranges.
        :download:`Fig1Cii.xml <../../sbml_files/Fig1Cii.xml>` for the provided example.

        Examples
        ---------
        >>> import crnt4sbml
        >>> network = crnt4sbml.CRNT("path/to/Fig1Cii.xml")
        >>> approach = network.get_semi_diffusive_approach()
        >>> bounds = approach.get_optimization_bounds()
        >>> print(bounds)
            [(0, 55), (0, 55), (0, 55), (0, 55), (0, 55), (0, 55), (0, 55), (0, 55), (0, 55), (0, 55), (0, 55), (0, 55)]
        """

        return [self.get_physiological_range("flux")]*len(self.get_decision_vector())

    def run_optimization(self, bounds=None, iterations=10, sys_min_val=numpy.finfo(float).eps, seed=0, print_flag=False,
                         numpy_dtype=numpy.float64, confidence_level_flag=False, change_in_rel_error=1e-2):
        """
        Function for running the optimization problem for the semi-diffusive approach. Note that there are no bounds
        enforced on species' concentrations as they are automatically restricted to be greater than zero by the theory.

        Parameters
        -----------
            bounds: list of tuples
                A list defining the lower and upper bounds for each variable in the decision vector. Here the reactions
                are allowed to be set to a single value.
            iterations: int
                The number of iterations to run the feasible point method.
            sys_min_val: float
                The value that should be considered zero for the optimization problem.
            seed: int
                Seed for the random number generator. None should be used if a random generation is desired.
            print_flag: bool
                Should be set to True if the user wants the objective function values found in the optimization problem
                and False otherwise.
            numpy_dtype:
                The numpy data type used within the optimization routine. All variables in the optimization routine will
                be converted to this data type.
            confidence_level_flag: bool
                If True a confidence level for the objective function will be given.
            change_in_rel_error: float
                The maximum relative error that should be allowed to consider :math:`f_k` in the neighborhood
                of :math:`\widetilde{f}`.
        Returns
        --------
        params_for_global_min: list of numpy arrays
            A list of numpy arrays that correspond to the decision vectors of the problem.
        obj_fun_val_for_params: list of floats
            A list of objective function values produced by the corresponding decision vectors in params_for_global_min.

        Examples
        ---------
        See :ref:`quickstart-injectivity-label` and :ref:`my-injectivity-label`.
        """
        temp_p = numpy.zeros(self.__N, numpy_dtype)
        self.__numpy_dtype = numpy_dtype

        # testing to see if there are any equalities in bounds
        equality_bounds_indices = []
        for i in range(len(bounds)):
            if not isinstance(bounds[i], tuple):
                equality_bounds_indices.append(i)
        
        # recasting user provided input to numpy_dtype
        for i in range(len(bounds)):
            bounds[i] = self.__numpy_dtype(bounds[i])
        sys_min_val = self.__numpy_dtype(sys_min_val)

        if equality_bounds_indices:
            print("Equalities in bounds is not allowed for injectivity approach!")
            sys.exit()

        params_for_global_min, obj_fun_val_for_params, self.__important_info = BistabilityFinder.run_optimization(
            bounds, iterations, sys_min_val, temp_p, self.__penalty_objective_func, self.__feasible_point_check,
            self.__objective_function_to_optimize, self.__final_constraint_check, seed, equality_bounds_indices,
            print_flag, numpy_dtype, [], confidence_level_flag, change_in_rel_error)

        return params_for_global_min, obj_fun_val_for_params

    def run_mpi_optimization(self, bounds=None, iterations=10, sys_min_val=numpy.finfo(float).eps, seed=0, print_flag=False,
                             numpy_dtype=numpy.float64, confidence_level_flag=False, change_in_rel_error=1e-2):
        """
        Function for running an mpi version of the optimization problem for the semi-diffusive approach. Note that there
        are no bounds enforced on species' concentrations as they are automatically restricted to be greater than
        zero by the theory.

        Parameters
        -----------
            bounds: list of tuples
                A list defining the lower and upper bounds for each variable in the decision vector. Here the reactions
                are allowed to be set to a single value.
            iterations: int
                The number of iterations to run the feasible point method.
            sys_min_val: float
                The value that should be considered zero for the optimization problem.
            seed: int
                Seed for the random number generator. None should be used if a random generation is desired.
            print_flag: bool
                Should be set to True if the user wants the objective function values found in the optimization problem
                and False otherwise.
            numpy_dtype:
                The numpy data type used within the optimization routine. All variables in the optimization routine will
                be converted to this data type.
            confidence_level_flag: bool
                If True a confidence level for the objective function will be given.
            change_in_rel_error: float
                The maximum relative error that should be allowed to consider :math:`f_k` in the neighborhood
                of :math:`\widetilde{f}`.
        Returns
        --------
        params_for_global_min: list of numpy arrays
            A list of numpy arrays that correspond to the decision vectors of the problem.
        obj_fun_val_for_params: list of floats
            A list of objective function values produced by the corresponding decision vectors in params_for_global_min.
        my_rank: integer
            An integer corresponding to the rank assigned to the core within the routine.

        Examples
        ---------
        See :ref:`parallel-crnt4sbml-label`.
        """
        temp_p = numpy.zeros(self.__N, numpy_dtype)
        self.__numpy_dtype = numpy_dtype

        # testing to see if there are any equalities in bounds
        equality_bounds_indices = []
        for i in range(len(bounds)):
            if not isinstance(bounds[i], tuple):
                equality_bounds_indices.append(i)

        # recasting user provided input to numpy_dtype
        for i in range(len(bounds)):
            bounds[i] = self.__numpy_dtype(bounds[i])
        sys_min_val = self.__numpy_dtype(sys_min_val)

        if equality_bounds_indices:
            print("Equalities in bounds is not allowed for injectivity approach!")
            sys.exit()

        params_for_global_min, obj_fun_val_for_params, self.__important_info, self.__my_rank, self.__comm, self.__num_cores = BistabilityFinder.run_mpi_optimization(
            bounds, iterations, sys_min_val, temp_p, self.__penalty_objective_func, self.__feasible_point_check,
            self.__objective_function_to_optimize, self.__final_constraint_check, seed, equality_bounds_indices,
            print_flag, numpy_dtype, [], confidence_level_flag, change_in_rel_error)

        return params_for_global_min, obj_fun_val_for_params, self.__my_rank

    def run_continuity_analysis(self, species=None, parameters=None, dir_path="./num_cont_graphs",
                                print_lbls_flag=False, auto_parameters=None, plot_labels=None):
        """
        Function for running the numerical continuation and bistability analysis portions of the semi-diffusive
        approach.

        Parameters
        ------------
            species: string
                A string stating the species that is the y-axis of the bifurcation diagram.
            parameters: list of numpy arrays
                A list of numpy arrays corresponding to the decision vectors that produce a small objective function
                value.
            dir_path: string
                A string stating the path where the bifurcation diagrams should be saved.
            print_lbls_flag: bool
                If True the routine will print the special points found by AUTO 2000 and False will not print any
                special points.
            auto_parameters: dict
                Dictionary defining the parameters for the AUTO 2000 run. Please note that one should **not** set
                'SBML' or 'ScanDirection' in these parameters as these are automatically assigned. It is absolutely
                necessary to set PrincipalContinuationParameter in this dictionary. For more information on these
                parameters refer to :download:`AUTO parameters <../auto2000_input.pdf>`. 'NMX' will default to
                10000 and 'ITMX' to 100.
            plot_labels: list of strings
                A list of strings defining the labels for the x-axis, y-axis, and title. Where the first element
                is the label for x-axis, second is the y-axis label, and the last element is the title label. If
                you would like to use the default settings for some of the labels, simply provide None for that
                element.
        Returns
        ---------
            multistable_param_ind: list of integers
                A list of those indices in 'parameters' that produce multistable plots.
            plot_specifications: list of lists
                A list whose elements correspond to the plot specifications of each element in multistable_param_ind.
                Each element is a list where the first element specifies the range used for the x-axis, the second
                element is the range for the y-axis, and the last element provides the x-y values and special point label
                for each special point in the plot.

        Example
        ---------
        See :ref:`quickstart-injectivity-label` and :ref:`my-injectivity-label`.
        """
        # setting defaults for AUTO
        if 'NMX' not in auto_parameters.keys():
            auto_parameters['NMX'] = 10000
            
        if 'ITMX' not in auto_parameters.keys():
            auto_parameters['ITMX'] = 100

        # making the directory if it doesn't exist
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)

        species_num = self.__species.index(species) + 1
        species_y = str(self.__species[species_num-1])

        multistable_param_ind, important_info, plot_specifications = BistabilityFinder.run_continuity_analysis(species_num, parameters,
                                                                                                               self.__initialize_ant_string,
                                                                                                               self.__finalize_ant_string,
                                                                                                               species_y, dir_path,
                                                                                                               print_lbls_flag,
                                                                                                               auto_parameters,
                                                                                                               plot_labels)

        self.__important_info += important_info

        return multistable_param_ind, plot_specifications

    # def run_mpi_continuity_analysis(self, species=None, parameters=None, dir_path="./num_cont_graphs",
    #                                 print_lbls_flag=False, auto_parameters=None, plot_labels=None):
    #     """
    #     Function for running the mpi numerical continuation and bistability analysis portions of the semi-diffusive
    #     approach.
    #
    #     Parameters
    #     ------------
    #         species: string
    #             A string stating the species that is the y-axis of the bifurcation diagram.
    #         parameters: list of numpy arrays
    #             A list of numpy arrays corresponding to the decision vectors that produce a small objective function
    #             value.
    #         dir_path: string
    #             A string stating the path where the bifurcation diagrams should be saved.
    #         print_lbls_flag: bool
    #             If True the routine will print the special points found by AUTO 2000 and False will not print any
    #             special points.
    #         auto_parameters: dict
    #             Dictionary defining the parameters for the AUTO 2000 run. Please note that one should **not** set
    #             'SBML' or 'ScanDirection' in these parameters as these are automatically assigned. It is absolutely
    #             necessary to set PrincipalContinuationParameter in this dictionary. For more information on these
    #             parameters refer to :download:`AUTO parameters <../auto2000_input.pdf>`. 'NMX' will default to
    #             10000 and 'ITMX' to 100.
    #         plot_labels: list of strings
    #             A list of strings defining the labels for the x-axis, y-axis, and title. Where the first element
    #             is the label for x-axis, second is the y-axis label, and the last element is the title label. If
    #             you would like to use the default settings for some of the labels, simply provide None for that
    #             element.
    #     Returns
    #     ---------
    #         multistable_param_ind: list of integers
    #             A list of those indices in 'parameters' that produce multistable plots.
    #         sample_portion: list of 1D numpy arrays
    #             A list of 1D numpy arrays corresponding to those values in the input variable parameters that was
    #             distributed to the core.
    #         plot_specifications: list of lists
    #             A list whose elements correspond to the plot specifications of each element in multistable_param_ind.
    #             Each element is a list where the first element specifies the range used for the x-axis, the second
    #             element is the range for the y-axis, and the last element provides the x-y values and special point label
    #             for each special point in the plot.
    #
    #     Example
    #     ---------
    #     See :ref:`quickstart-injectivity-label` and :ref:`my-injectivity-label`.
    #     """
    #     # setting defaults for AUTO
    #     if 'NMX' not in auto_parameters.keys():
    #         auto_parameters['NMX'] = 10000
    #
    #     if 'ITMX' not in auto_parameters.keys():
    #         auto_parameters['ITMX'] = 100
    #
    #     # making the directory if it doesn't exist
    #     if not os.path.isdir(dir_path) and self.__my_rank == 0:
    #         os.mkdir(dir_path)
    #
    #     species_num = self.__species.index(species) + 1
    #     species_y = str(self.__species[species_num - 1])
    #
    #     if self.__comm is not None:
    #         sample_portion = self.__distribute_list_of_points(parameters)
    #         self.__comm.Barrier()
    #     else:
    #
    #         from mpi4py import MPI
    #         self.__comm = MPI.COMM_WORLD
    #         self.__my_rank = self.__comm.Get_rank()
    #         self.__num_cores = self.__comm.Get_size()
    #         self.__comm.Barrier()
    #
    #         if not os.path.isdir(dir_path) and self.__my_rank == 0:
    #             os.mkdir(dir_path)
    #         sample_portion = self.__distribute_list_of_points(parameters)
    #         self.__comm.Barrier()
    #
    #     multistable_param_ind, important_info, plot_specifications = BistabilityFinder.run_mpi_continuity_analysis(
    #         species_num, sample_portion,
    #         self.__initialize_ant_string,
    #         self.__finalize_ant_string,
    #         species_y, dir_path,
    #         print_lbls_flag,
    #         auto_parameters,
    #         plot_labels, self.__my_rank, self.__comm)
    #
    #     self.__important_info += important_info
    #
    #     return multistable_param_ind, sample_portion, plot_specifications

    def run_greedy_continuity_analysis(self, species=None, parameters=None, dir_path="./num_cont_graphs",
                                       print_lbls_flag=False, auto_parameters=None, plot_labels=None):
        """
        Function for running the greedy numerical continuation and bistability analysis portions of the semi-diffusive
        approach. This routine uses the initial value of the principal continuation parameter to construct AUTO
        parameters and then tests varying fixed step sizes for the continuation problem. Note that this routine may
        produce jagged or missing sections in the plots provided. To produce better plots one should use the information
        provided by this routine to run :func:`crnt4sbml.SemiDiffusiveApproach.run_continuity_analysis`.

        Parameters
        ------------
            species: string
                A string stating the species that is the y-axis of the bifurcation diagram.
            parameters: list of numpy arrays
                A list of numpy arrays corresponding to the decision vectors that produce a small objective function
                value.
            dir_path: string
                A string stating the path where the bifurcation diagrams should be saved.
            print_lbls_flag: bool
                If True the routine will print the special points found by AUTO 2000 and False will not print any
                special points.
            auto_parameters: dict
                Dictionary defining the parameters for the AUTO 2000 run. Please note that only the
                PrincipalContinuationParameter in this dictionary should be defined, no other AUTO parameters should
                be set. For more information on these parameters refer to :download:`AUTO parameters <../auto2000_input.pdf>`.
            plot_labels: list of strings
                A list of strings defining the labels for the x-axis, y-axis, and title. Where the first element
                is the label for x-axis, second is the y-axis label, and the last element is the title label. If
                you would like to use the default settings for some of the labels, simply provide None for that
                element.
        Returns
        ---------
            multistable_param_ind: list of integers
                A list of those indices in 'parameters' that produce multistable plots.
            plot_specifications: list of lists
                A list whose elements correspond to the plot specifications of each element in multistable_param_ind.
                Each element is a list where the first element specifies the range used for the x-axis, the second
                element is the range for the y-axis, and the last element provides the x-y values and special point label
                for each special point in the plot.

        Example
        ---------
        See :ref:`my-injectivity-label`.
        """
        # setting defaults for AUTO
        if 'NMX' not in auto_parameters.keys():
            auto_parameters['NMX'] = 10000

        if 'ITMX' not in auto_parameters.keys():
            auto_parameters['ITMX'] = 100

        # making the directory if it doesn't exist
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)

        species_num = self.__species.index(species) + 1
        species_y = str(self.__species[species_num - 1])

        multistable_param_ind, important_info, plot_specifications = BistabilityFinder.run_greedy_continuity_analysis\
            (species_num, parameters, self.__initialize_ant_string, self.__finalize_ant_string, species_y, dir_path,
             print_lbls_flag, auto_parameters, plot_labels)

        self.__important_info += important_info

        return multistable_param_ind, plot_specifications

    # def run_mpi_greedy_continuity_analysis(self, species=None, parameters=None, dir_path="./num_cont_graphs",
    #                                        print_lbls_flag=False, auto_parameters=None, plot_labels=None):
    #     """
    #     Function for running the mpi greedy numerical continuation and bistability analysis portions of the semi-diffusive
    #     approach. This routine uses the initial value of the principal continuation parameter to construct AUTO
    #     parameters and then tests varying fixed step sizes for the continuation problem. Note that this routine may
    #     produce jagged or missing sections in the plots provided. To produce better plots one should use the information
    #     provided by this routine to run :func:`crnt4sbml.SemiDiffusiveApproach.run_continuity_analysis`.
    #
    #     Parameters
    #     ------------
    #         species: string
    #             A string stating the species that is the y-axis of the bifurcation diagram.
    #         parameters: list of numpy arrays
    #             A list of numpy arrays corresponding to the decision vectors that produce a small objective function
    #             value.
    #         dir_path: string
    #             A string stating the path where the bifurcation diagrams should be saved.
    #         print_lbls_flag: bool
    #             If True the routine will print the special points found by AUTO 2000 and False will not print any
    #             special points.
    #         auto_parameters: dict
    #             Dictionary defining the parameters for the AUTO 2000 run. Please note that only the
    #             PrincipalContinuationParameter in this dictionary should be defined, no other AUTO parameters should
    #             be set. For more information on these parameters refer to :download:`AUTO parameters <../auto2000_input.pdf>`.
    #         plot_labels: list of strings
    #             A list of strings defining the labels for the x-axis, y-axis, and title. Where the first element
    #             is the label for x-axis, second is the y-axis label, and the last element is the title label. If
    #             you would like to use the default settings for some of the labels, simply provide None for that
    #             element.
    #     Returns
    #     ---------
    #         multistable_param_ind: list of integers
    #             A list of those indices in 'parameters' that produce multistable plots.
    #         sample_portion: list of 1D numpy arrays
    #             A list of 1D numpy arrays corresponding to those values in the input variable parameters that was
    #             distributed to the core.
    #         plot_specifications: list of lists
    #             A list whose elements correspond to the plot specifications of each element in multistable_param_ind.
    #             Each element is a list where the first element specifies the range used for the x-axis, the second
    #             element is the range for the y-axis, and the last element provides the x-y values and special point label
    #             for each special point in the plot.
    #
    #     Example
    #     ---------
    #     See :ref:`my-injectivity-label`.
    #     """
    #     # setting defaults for AUTO
    #     if 'NMX' not in auto_parameters.keys():
    #         auto_parameters['NMX'] = 10000
    #
    #     if 'ITMX' not in auto_parameters.keys():
    #         auto_parameters['ITMX'] = 100
    #
    #     # making the directory if it doesn't exist
    #     if not os.path.isdir(dir_path) and self.__my_rank == 0:
    #         os.mkdir(dir_path)
    #
    #     species_num = self.__species.index(species) + 1
    #     species_y = str(self.__species[species_num - 1])
    #
    #     if self.__comm is not None:
    #         sample_portion = self.__distribute_list_of_points(parameters)
    #         self.__comm.Barrier()
    #     else:
    #
    #         from mpi4py import MPI
    #         self.__comm = MPI.COMM_WORLD
    #         self.__my_rank = self.__comm.Get_rank()
    #         self.__num_cores = self.__comm.Get_size()
    #         self.__comm.Barrier()
    #
    #         if not os.path.isdir(dir_path) and self.__my_rank == 0:
    #             os.mkdir(dir_path)
    #         sample_portion = self.__distribute_list_of_points(parameters)
    #         self.__comm.Barrier()
    #
    #     multistable_param_ind, important_info, plot_specifications = BistabilityFinder.run_mpi_greedy_continuity_analysis\
    #         (species_num, sample_portion, self.__initialize_ant_string, self.__finalize_ant_string, species_y, dir_path,
    #          print_lbls_flag, auto_parameters, plot_labels, self.__my_rank, self.__comm)
    #
    #     self.__important_info += important_info
    #
    #     return multistable_param_ind, sample_portion, plot_specifications

    def __distribute_list_of_points(self, samples):

        if self.__my_rank == 0:

            # number of tasks per core
            tasks = len(samples) // self.__num_cores  # // calculates the floor

            # remainder
            r = len(samples) - self.__num_cores * tasks

            # array that holds how many tasks each core has
            tasks_core = numpy.zeros(self.__num_cores, dtype=numpy.int64)
            tasks_core.fill(tasks)

            # distributing in the remainder
            ii = 0
            while r > 0:
                tasks_core[ii] += 1
                r -= 1
                ii += 1

            sample_portion = samples[0:tasks_core[0]]

            if self.__num_cores > 1:
                for i in range(1, self.__num_cores):
                    start = sum(tasks_core[0:i])
                    end = start + tasks_core[i]
                    self.__comm.send(samples[start:end], dest=i, tag=i * 11)

        else:
            if self.__num_cores > 1:
                sample_portion = self.__comm.recv(source=0, tag=self.__my_rank * 11)

        return sample_portion

    def __initialize_ant_string(self, species_num, pcp_x_reaction):
        self.__create_reaction_rates_vector()

        self.__inflow_vector = sympy.zeros(self.__N, 1)

        edges_inflow = [list(self.__g_edges).index(e) for e in self.__g_edges if e[0] in self.__var_nothing_index]

        [self.__p_symbols.append(sympy.Symbol('p' + str(i))) for i in edges_inflow]

        count = len(self.__edges_true_outflow)
        for i in self.__key_species_indices:
            self.__inflow_vector[i] = self.__p_symbols[count]
            count += 1

        self.__ode = self.__inflow_vector + self.__S_to*self.__reaction_rates_vector

        ode_str = 'var species ' + str(self.__species[species_num-1])
        for i in range(self.__N):
            if self.__species[i] != self.__species[species_num-1]:
                ode_str += ',' + str(self.__species[i])
        ode_str += '; ' 

        for i in range(self.__N):
            ode_str += 'J' + str(i) + ': -> ' + str(self.__species[i]) + '; ' + str(self.__ode[i]) + '; ' 

        # replacing any powers with ^ instead of **
        ode_str = ode_str.replace('**', '^')

        self.__S_to_numpy = numpy.array(self.__S_to).astype(numpy.float64)
        
        # finding the PCP in terms of P_symbols rather than reaction
        edges_indices = self.__edges_true_outflow + edges_inflow
        edge_labels = [self.__g.edges[list(self.__g_edges)[i]]['label'] for i in edges_indices]
        pcp_index = edge_labels.index(pcp_x_reaction)
        pcp_x = str(self.__p_symbols[pcp_index])

        return ode_str, pcp_x

    def __create_reaction_rates_vector(self):
        source_species = [self.__g.nodes[list(self.__g_nodes)[i]]['species'] for i in self.__sources_true_outflow]
        
        source_stoichiometries = [self.__g.nodes[list(self.__g_nodes)[i]]['stoichiometries']
                                  for i in self.__sources_true_outflow]

        self.__p_symbols = [sympy.Symbol('p' + str(i)) for i in self.__edges_true_outflow]

        self.__reaction_rates_vector = sympy.zeros(len(self.__p_symbols), 1)
        for i in range(len(self.__p_symbols)):
            temp_list = [sympy.Symbol(source_species[i][j])**source_stoichiometries[i][j]
                         for j in range(len(source_species[i]))]
            temp_val = 1
            for j in range(len(source_species[i])):
                temp_val *= temp_list[j]
            self.__reaction_rates_vector[i] = self.__p_symbols[i]*temp_val

    def __finalize_ant_string(self, x, ode_str):
        p = -self.__S_to_numpy.dot(x)

        for i in range(len(x)):
            ode_str += str(self.__p_symbols[i]) + ' = ' + str(x[i]) + ';'
        temp = [p[i] for i in self.__key_species_indices]
        count = 0
        
        for i in range(len(x), len(self.__p_symbols)):
            ode_str += str(self.__p_symbols[i]) + ' = ' + str(temp[count]) + ';'
            count += 1 

        lam_ode = []
        temp_sym = self.__p_symbols[:]
        temp_sym += self.__concentration_pars[:]

        for i in range(len(self.__ode)):
            lam_ode.append(sympy.utilities.lambdify(temp_sym, self.__ode[i], 'numpy'))

        for i in range(self.__N):
            ode_str += str(self.__species[i]) + ' = ' + str(1.0) + ';'

        return ode_str

    def __penalty_objective_func(self, x_initial, temp_p, penalty_bounds, equality_bounds_indices, x,
                                 non_equality_bounds_indices, concentration_bounds):
        equality_constraints = numpy.zeros(len(self.__mus_solved_for), dtype=self.__numpy_dtype)
        for i in range(len(self.__mus_solved_for)):
            equality_constraints[i] = self.__lambda_equality_poly_fun[i](*tuple(x_initial))
            
        x = numpy.zeros(len(self.__mu_vec), dtype=self.__numpy_dtype)
        count = 0 
        for j in self.__mus_solved_for_indices:
            x[j] = equality_constraints[count]
            count += 1 

        count = 0 
        for j in self.__decision_vector_indices:
            x[j] = x_initial[count]
            count += 1 

        temp = numpy.zeros(len(self.__key_species_indices), dtype=self.__numpy_dtype)
        count = 0
        for i in self.__key_species_indices:
            temp[count] = numpy.maximum(self.__numpy_dtype(0.0), -self.__lambda_poly_func[i](*tuple(x)))**2
            count += 1

        sum1 = numpy.sum(temp)

        temp = numpy.zeros(len(self.__non_key_species_indices), dtype=self.__numpy_dtype)
        count = 0
        for j in self.__mus_solved_for_indices:
            temp[count] = numpy.maximum(self.__numpy_dtype(0.0), -x[j])**2
            count += 1

        sum2 = numpy.sum(temp)

        sum0 = self.__numpy_dtype(0.0)
        for j in non_equality_bounds_indices:

            sum0 += numpy.maximum(self.__numpy_dtype(0.0), penalty_bounds[j][0]-x_initial[j])**2

            sum0 += numpy.maximum(self.__numpy_dtype(0.0), x_initial[j] - penalty_bounds[j][1])**2

        sumval = sum1+sum2 + sum0

        return sumval 

    def __feasible_point_check(self, x_initial, result_fun, sys_min_val, equality_bounds_indices,
                               non_equality_bounds_indices, penalty_bounds, concentration_bounds):
        finite_chk = numpy.isfinite(x_initial)
        if numpy.all(finite_chk):
            
            test = []
            for j in non_equality_bounds_indices:
                test.append(x_initial[j] >= penalty_bounds[j][0] and x_initial[j] <= penalty_bounds[j][1])
            boundry_chk = numpy.all(test)

            equality_constraints = numpy.zeros(len(self.__mus_solved_for), dtype=self.__numpy_dtype)
            all_constraints = []
            for i in range(len(self.__mus_solved_for)):
                equality_constraints[i] = self.__lambda_equality_poly_fun[i](*tuple(x_initial))
                all_constraints.append(equality_constraints[i])

            x = numpy.zeros(len(self.__mu_vec), dtype=self.__numpy_dtype)
            count = 0
            for j in self.__mus_solved_for_indices:
                x[j] = equality_constraints[count]
                count += 1

            count = 0
            for j in self.__decision_vector_indices:
                x[j] = x_initial[count]
                count += 1    

            for i in self.__key_species_indices:  
                all_constraints.append(self.__lambda_poly_func[i](*tuple(x)))

            constraints_chk = all([i > self.__numpy_dtype(0.0) for i in all_constraints])

            # putting the feasible points in x_candidates
            if (abs(result_fun) <= self.__numpy_dtype(1e-200)) and boundry_chk and constraints_chk: 
                return [True, x_initial]
            else:
                return [False, x_initial]
        else:
            return [False, x_initial]

    def __objective_function_to_optimize(self, x_initial, temp_c, penalty_bounds, sys_min_val, equality_bounds_indices,
                                         x, non_equality_bounds_indices, concentration_bounds):
        test = []
        for j in non_equality_bounds_indices:
            test.append(x_initial[j] >= penalty_bounds[j][0] and x_initial[j] <= penalty_bounds[j][1])
        boundry_chk = numpy.all(test)

        if boundry_chk:

            equality_constraints = numpy.zeros(len(self.__mus_solved_for), dtype=self.__numpy_dtype)
            all_constraints = []
            for i in range(len(self.__mus_solved_for)):
                equality_constraints[i] = self.__lambda_equality_poly_fun[i](*tuple(x_initial))
                all_constraints.append(equality_constraints[i])

            x = numpy.zeros(len(self.__mu_vec), dtype=self.__numpy_dtype)
            count = 0
            for j in self.__mus_solved_for_indices:
                x[j] = equality_constraints[count]
                count += 1

            count = 0
            for j in self.__decision_vector_indices:
                x[j] = x_initial[count]
                count += 1

            for i in self.__key_species_indices:
                all_constraints.append(self.__lambda_poly_func[i](*tuple(x)))

            constraints_chk = all([i > self.__numpy_dtype(0.0) for i in all_constraints])

            if constraints_chk:
                return self.__lambda_objective_fun(*tuple(x))
            else:
                return numpy.PINF
        else:
            return numpy.PINF

    def __final_constraint_check(self, x_initial, penalty_bounds, sys_min_val, equality_bounds_indices,
                                 concentration_bounds):
        non_equality_bounds_indices = [i for i in range(len(penalty_bounds)) if i not in equality_bounds_indices]

        test = []
        for j in non_equality_bounds_indices:
            test.append(x_initial[j] >= penalty_bounds[j][0] and x_initial[j] <= penalty_bounds[j][1])
        boundry_chk = numpy.all(test)

        equality_constraints = numpy.zeros(len(self.__mus_solved_for), dtype=self.__numpy_dtype)
        all_constraints = []
        for i in range(len(self.__mus_solved_for)):
            equality_constraints[i] = self.__lambda_equality_poly_fun[i](*tuple(x_initial))
            all_constraints.append(equality_constraints[i])

        x = numpy.zeros(len(self.__mu_vec), dtype=self.__numpy_dtype)
        count = 0
        for j in self.__mus_solved_for_indices:
            x[j] = equality_constraints[count]
            count += 1

        count = 0
        for j in self.__decision_vector_indices:
            x[j] = x_initial[count]
            count += 1

        for i in self.__key_species_indices:
            all_constraints.append(self.__lambda_poly_func[i](*tuple(x)))

        constraints_chk = all([i > self.__numpy_dtype(0.0) for i in all_constraints])

        # must convert x to numpy.float64 because higher
        # is not supported in linalg
        x_converted = numpy.float64(x)

        rank_jacobian = numpy.linalg.matrix_rank(self.__lambda_J(*tuple(x_converted)))

        rank_jacobian_chk = rank_jacobian == self.__N - 1

        if constraints_chk and boundry_chk and rank_jacobian_chk:
            return [True, x]

        else:
            return [False, []]

    def __create_y_r_matrix(self):
        self.__sources_true_outflow = [list(self.__g_nodes).index(e[0]) for e in self.__g_edges if e[0]
                                       not in self.__var_nothing_index]
        self.__Y_r = sympy.zeros(self.__N, len(self.__sources_true_outflow))

        for i in range(len(self.__sources_true_outflow)):
            self.__Y_r[:, i] = self.__cgraph.get_y()[:, self.__sources_true_outflow[i]]

    def __create_s_to_matrix(self):
        self.__edges_true_outflow = [list(self.__g_edges).index(e) for e in self.__g_edges if
                                     (e[1] in self.__var_nothing_index) or (e[0] not in self.__var_nothing_index)]

        self.__S_to = sympy.zeros(self.__N, len(self.__edges_true_outflow))

        for i in range(len(self.__edges_true_outflow)): 
            self.__S_to[:, i] = self.__cgraph.get_s()[:, self.__edges_true_outflow[i]]

    def __create_symbolic_jacobian_matrix(self):
        self.__mu_vec = [sympy.symbols('v_' + str(i+1)) for i in self.__edges_true_outflow]

        diag_mu = sympy.diag(*self.__mu_vec)

        self.__symbolic_J = self.__S_to*diag_mu*self.__Y_r.T

    def __create_lambda_jacobian_matrix(self):
        self.__lambda_J = sympy.utilities.lambdify(self.__mu_vec, self.__symbolic_J, 'numpy')

    def __create_symbolic_objective_function(self):
        self.__symbolic_objective_fun = (self.__symbolic_J.det(method='lu'))**2

    def __create_lambda_objective_function(self):
        self.__lambda_objective_fun = sympy.utilities.lambdify(self.__mu_vec, self.__symbolic_objective_fun, 'numpy')

    def __create_symbolic_polynomial_function(self):
        mu_sym_mat = sympy.Matrix([[mu] for mu in self.__mu_vec])
        self.__symbolic_poly_func = -self.__S_to*mu_sym_mat
        
    def __create_lambda_polynomial_function(self):
        self.__lambda_poly_func = []
        for i in range(self.__N):
            self.__lambda_poly_func += [sympy.utilities.lambdify(self.__mu_vec, self.__symbolic_poly_func[i], 'numpy')]

    def __create_lambda_equality_poly_fun(self):
        self.__lambda_equality_poly_fun = []
        for i in range(len(self.__mus_solved_for)):
            self.__lambda_equality_poly_fun += [sympy.utilities.lambdify(self.__decision_vector,
                                                                         self.__symbolic_equality_poly_fun[i][0],
                                                                         'numpy')]

    def __find_key_species_indices(self):
        key_species_vertex = []
        for e in self.__g_edges:
            if e[0] in self.__var_nothing_index:
                key_species_vertex.append(e[1])

        # putting key_species in order
        key_species = [i for i in self.__species if i in key_species_vertex]

        self.__key_species_indices = [self.__species.index(i) for i in key_species]

    def __find_non_key_species_indices(self):
        self.__non_key_species_indices = [i for i in range(len(self.__species)) if i not in self.__key_species_indices]

    def __create_concentration_pars(self):
        self.__concentration_pars = [sympy.Symbol(self.__species[i]) for i in range(self.__N)]

    def __create_decision_vector(self):
        atoms_of_p_non_key = []
        for i in self.__non_key_species_indices:
            atoms_of_p_non_key.append(self.__symbolic_poly_func[i].atoms(sympy.Symbol))

        available_mus = list(set.union(*atoms_of_p_non_key))

        # putting them in order for the sake of reproducibility
        available_mus = [i for i in self.__mu_vec if i in available_mus]

        # putting them in order for the sake of reproducibility
        for i in range(len(atoms_of_p_non_key)):
            atoms_of_p_non_key[i] = [j for j in self.__mu_vec if j in atoms_of_p_non_key[i]]

        self.__mus_solved_for = []
        for i in range(len(atoms_of_p_non_key)):
            for j in atoms_of_p_non_key[i]:
                if j in available_mus:
                    if not any([j in atoms_of_p_non_key[ii] for ii in range(len(atoms_of_p_non_key)) if i != ii]):
                    
                        self.__mus_solved_for.append(j)
                        available_mus.remove(j)
                        break
                    
        self.__symbolic_equality_poly_fun = []
        count = 0
        for i in self.__non_key_species_indices:
            self.__symbolic_equality_poly_fun.append(sympy.solve(self.__symbolic_poly_func[i],
                                                                 self.__mus_solved_for[count]))
            count += 1

        variables_in_decision_vector = list(set(self.__mu_vec) - set(self.__mus_solved_for))

        self.__decision_vector = [i for i in self.__mu_vec if i in variables_in_decision_vector]

        true_outflow_reaction_labels = [self.__g.edges[list(self.__g_edges)[i]]['label']
                                        for i in self.__edges_true_outflow]

        self.__decision_vector_indices = [self.__mu_vec.index(i) for i in self.__decision_vector]

        self.__mus_solved_for_indices = [self.__mu_vec.index(i) for i in self.__mus_solved_for]

        self.__decision_vector_reaction_labels = [true_outflow_reaction_labels[i]
                                                  for i in self.__decision_vector_indices]

    # getters
    def get_y_r_matrix(self):
        """
        Returns SymPy matrix representing the :math:`Y_r` matrix. The columns of which correspond to the true and
        outflow reactions of the molecularity matrix.
        :download:`Fig1Cii.xml <../../sbml_files/Fig1Cii.xml>` for the provided
        example.

        Example
        --------
        >>> import crnt4sbml
        >>> import sympy
        >>> network = crnt4sbml.CRNT("path/to/Fig1Cii.xml")
        >>> approach = network.get_semi_diffusive_approach()
        >>> sympy.pprint(approach.get_y_r_matrix())
            ⎡1  0  0  0  1  0  0  0  0  1  0  0  0  0  0  0⎤
            ⎢                                              ⎥
            ⎢1  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0⎥
            ⎢                                              ⎥
            ⎢0  1  0  0  0  0  1  0  0  0  0  0  0  1  0  0⎥
            ⎢                                              ⎥
            ⎢0  0  1  0  1  0  0  0  0  0  0  0  1  0  0  0⎥
            ⎢                                              ⎥
            ⎢0  0  1  0  0  0  0  0  0  0  0  1  0  0  0  0⎥
            ⎢                                              ⎥
            ⎢0  0  0  1  0  0  0  1  0  0  0  0  0  0  1  0⎥
            ⎢                                              ⎥
            ⎣0  0  0  0  0  1  0  0  1  0  0  0  0  0  0  1⎦
        """
        return self.__Y_r

    def get_s_to_matrix(self):
        """
        Returns SymPy matrix representing the :math:`S_{to}` matrix. The columns of which correspond to the true and
        outflow reactions of the stoichiometric matrix.
        :download:`Fig1Cii.xml <../../sbml_files/Fig1Cii.xml>` for the provided
        example.

        Example
        --------
        >>> import crnt4sbml
        >>> import sympy
        >>> network = crnt4sbml.CRNT("path/to/Fig1Cii.xml")
        >>> approach = network.get_semi_diffusive_approach()
        >>> sympy.pprint(approach.get_s_to_matrix())
            ⎡-1  1   0   0   -1  1   0   1   0   -1  0   0   0   0   0   0 ⎤
            ⎢                                                              ⎥
            ⎢-1  1   0   0   0   0   1   0   0   0   -1  0   0   0   0   0 ⎥
            ⎢                                                              ⎥
            ⎢1   -1  0   0   0   0   -1  0   0   0   0   0   0   -1  0   0 ⎥
            ⎢                                                              ⎥
            ⎢0   0   -1  1   -1  1   1   0   2   0   0   0   -1  0   0   0 ⎥
            ⎢                                                              ⎥
            ⎢0   0   -1  1   0   0   0   1   0   0   0   -1  0   0   0   0 ⎥
            ⎢                                                              ⎥
            ⎢0   0   1   -1  0   0   0   -1  0   0   0   0   0   0   -1  0 ⎥
            ⎢                                                              ⎥
            ⎣0   0   0   0   1   -1  0   0   -1  0   0   0   0   0   0   -1⎦
        """
        return self.__S_to    

    def get_symbolic_objective_fun(self):
        """
        Returns SymPy expression for the objective function of the optimization problem. This is the determinant of
        :math:`S_{to}diag(\mu)Y_r^T` squared.

        Example
        --------
        >>> import crnt4sbml
        >>> network = crnt4sbml.CRNT("path/to/sbml_file.xml")
        >>> approach = network.get_semi_diffusive_approach()
        >>> approach.get_symbolic_objective_fun()
        """
        return self.__symbolic_objective_fun

    def get_lambda_objective_fun(self):
        """
        Returns a lambda function representation of the objective function of the optimization problem. Here the
        arguments of the lambda function are given by the values provided by
        :func:`crnt4sbml.SemiDiffusiveApproach.get_mu_vector`.

        Example
        --------
        >>> import crnt4sbml
        >>> network = crnt4sbml.CRNT("path/to/sbml_file.xml")
        >>> approach = network.get_semi_diffusive_approach()
        >>> approach.get_lambda_objective_fun()
        """
        return self.__lambda_objective_fun

    def get_symbolic_polynomial_fun(self):
        """
        Returns SymPy matrix representing the vector of polynomial functions, :math:`-S_{to} \mu`.
        :download:`Fig1Cii.xml <../../sbml_files/Fig1Cii.xml>` for the provided
        example.

        Example
        --------
        >>> import crnt4sbml
        >>> import sympy
        >>> network = crnt4sbml.CRNT("path/to/Fig1Cii.xml")
        >>> approach = network.get_semi_diffusive_approach()
        >>> sympy.pprint(approach.get_symbolic_polynomial_fun())
            ⎡   v₁ + v₁₁ - v₂ + v₅ - v₆ - v₈    ⎤
            ⎢                                   ⎥
            ⎢        v₁ + v₁₃ - v₂ - v₇         ⎥
            ⎢                                   ⎥
            ⎢        -v₁ + v₁₇ + v₂ + v₇        ⎥
            ⎢                                   ⎥
            ⎢v₁₆ + v₃ - v₄ + v₅ - v₆ - v₇ - 2⋅v₉⎥
            ⎢                                   ⎥
            ⎢        v₁₅ + v₃ - v₄ - v₈         ⎥
            ⎢                                   ⎥
            ⎢        v₁₈ - v₃ + v₄ + v₈         ⎥
            ⎢                                   ⎥
            ⎣        v₁₉ - v₅ + v₆ + v₉         ⎦
        """
        return self.__symbolic_poly_func

    def get_lambda_polynomial_fun(self):
        """
        Returns a list of lambda functions for the vector of polynomial functions. The index of the list corresponds to
        the row in the vector of polynomial functions. Here the arguments of the lambda function are given by the values
        provided by :func:`crnt4sbml.SemiDiffusiveApproach.get_mu_vector`.

        Example
        --------
        >>> import crnt4sbml
        >>> network = crnt4sbml.CRNT("path/to/sbml_file.xml")
        >>> approach = network.get_semi_diffusive_approach()
        >>> approach.get_lambda_polynomial_fun()
        """
        return self.__lambda_poly_func

    def get_key_species(self):
        """
        Returns a list of string variables corresponding to the key species.
        :download:`Fig1Cii.xml <../../sbml_files/Fig1Cii.xml>` for the provided
        example.

        Example
        --------
        >>> import crnt4sbml
        >>> network = crnt4sbml.CRNT("path/to/Fig1Cii.xml")
        >>> approach = network.get_semi_diffusive_approach()
        >>> print(approach.get_key_species())
            ['s1', 's2', 's7']
        """
        return [self.__species[i] for i in self.__key_species_indices]

    def get_non_key_species(self):
        """
        Returns a list of string variables corresponding to those species that are not key species.
        :download:`Fig1Cii.xml <../../sbml_files/Fig1Cii.xml>` for the provided
        example.

        Example
        --------
        >>> import crnt4sbml
        >>> network = crnt4sbml.CRNT("path/to/Fig1Cii.xml")
        >>> approach = network.get_semi_diffusive_approach()
        >>> print(approach.get_non_key_species())
            ['s3', 's6', 's8', 's11']
        """
        return [self.__species[i] for i in self.__non_key_species_indices]

    def get_boundary_species(self):
        """
        Returns a list of string variables corresponding to those species that are defined as boundary species.
        :download:`Fig1Cii.xml <../../sbml_files/Fig1Cii.xml>` for the provided
        example.

        Example
        --------
        >>> import crnt4sbml
        >>> network = crnt4sbml.CRNT("path/to/Fig1Cii.xml")
        >>> approach = network.get_semi_diffusive_approach()
        >>> print(approach.get_boundary_species())
            ['s21']
        """
        return [i for i in self.__var_nothing_index]

    def get_decision_vector(self):
        """
        Returns a list of SymPy variables corresponding to the decision vector for the optimization problem.
        :download:`Fig1Cii.xml <../../sbml_files/Fig1Cii.xml>` for the provided
        example.

        Example
        --------
        >>> import crnt4sbml
        >>> network = crnt4sbml.CRNT("path/to/Fig1Cii.xml")
        >>> approach = network.get_semi_diffusive_approach()
        >>> print(approach.get_decision_vector())
            [v_2, v_3, v_4, v_5, v_6, v_7, v_9, v_11, v_13, v_15, v_17, v_18]

        See also
        ----------
        crnt4sbml.SemiDiffusiveApproach.print_decision_vector
        """
        return self.__decision_vector

    def get_mu_vector(self):
        """
        Returns a list of SymPy variables corresponding to the vector of fluxes, :math:`\mu` .
        :download:`Fig1Cii.xml <../../sbml_files/Fig1Cii.xml>` for the provided
        example.

        Example
        --------
        >>> import crnt4sbml
        >>> network = crnt4sbml.CRNT("path/to/Fig1Cii.xml")
        >>> approach = network.get_semi_diffusive_approach()
        >>> print(approach.get_mu_vector())
            [v_1, v_2, v_3, v_4, v_5, v_6, v_7, v_8, v_9, v_11, v_13, v_15, v_16, v_17, v_18, v_19]
        """
        return self.__mu_vec

    def print_decision_vector(self):
        """
        Prints an easily readable form of the decision vector. It first prints the decision vector and then the
        corresponding reaction labels.
        :download:`Fig1Cii.xml <../../sbml_files/Fig1Cii.xml>` for the provided
        example.

        Example
        --------
        >>> import crnt4sbml
        >>> network = crnt4sbml.CRNT("path/to/Fig1Cii.xml")
        >>> approach = network.get_semi_diffusive_approach()
        >>> approach.print_decision_vector()
            Decision vector for optimization:
            [v_2, v_3, v_4, v_5, v_6, v_7, v_9, v_11, v_13, v_15, v_17, v_18]
            Reaction labels for decision vector:
            ['re1r', 're3', 're3r', 're6', 're6r', 're2', 're8', 're17r', 're18r', 're19r', 're21', 're22']
        """
        print("Decision vector for optimization: ")
        print(self.__decision_vector)
        print("")
        print("Reaction labels for decision vector: ")
        print(self.__decision_vector_reaction_labels)
        print("")

    def generate_report(self):
        """
        Prints out helpful details constructed by :func:`crnt4sbml.SemiDiffusiveApproach.run_optimization` and
        :func:`crnt4sbml.SemiDiffusiveApproach.run_continuity_analysis`.

        Example
        --------
        See :ref:`quickstart-injectivity-label` and :ref:`my-injectivity-label`.
        """
        #print(self.__important_info)

        if self.__comm == None:
            print(self.__important_info)
        else:

            all_important_info = self.__comm.gather(self.__important_info, root=0)
            self.__comm.Barrier()

            if self.__my_rank == 0:

                print("")

                for i in range(1, len(all_important_info)):
                    print(all_important_info[i])
                print(self.__important_info)

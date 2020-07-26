"""Handle pc by reparametrizations."""
import estimagic.optimization.kernel_transformations as kt


def reparametrize_to_internal(external, internal_free, processed_constraints):
    """Convert a params DataFrame into a numpy array of internal parameters.

    Args:
        processed_params (DataFrame): A processed params DataFrame. See :ref:`params`.
        processed_constraints (list): Processed and consolidated pc.

    Returns:
        internal_params (numpy.ndarray): 1d numpy array of free reparametrized
            parameters.

    """
    internal_values = external.copy()
    for constr in processed_constraints:
        func = getattr(kt, f"{constr['type']}_to_internal")

        internal_values[constr["index"]] = func(external[constr["index"]], constr)

    return internal_values[internal_free]


def reparametrize_from_internal(
    internal, fixed_values, pre_replacements, processed_constraints, post_replacements,
):
    """Convert a numpy array of internal parameters to a params DataFrame.

    Args:
        internal (numpy.ndarray): 1d numpy array with internal parameters
        fixed_values (numpy.ndarray): 1d numpy array with internal fixed values
        pre_replacements (numpy.ndarray): 1d numpy array with positions of internal
            parameters that have to be copied before transformations are applied.
            Negative if no value has to be copied.
        processed_constraints (list): List of processed and consolidated constraint
            dictionaries. Can have the types "linear", "probability", "covariance"
            and "sdcorr".
        post_replacments (numpy.ndarray): 1d numpy array with parameter positions.

    Returns:
        numpy.ndarray: Array with external parameters

    """
    external_values = fixed_values.copy()

    # do pre-replacements
    mask = pre_replacements >= 0
    positions = pre_replacements[mask]
    external_values[mask] = internal[positions]

    # do transformations
    for constr in processed_constraints:
        func = getattr(kt, f"{constr['type']}_from_internal")
        external_values[constr["index"]] = func(
            external_values[constr["index"]], constr
        )

    # do post-replacements
    mask = post_replacements >= 0
    positions = post_replacements[mask]
    external_values[mask] = external_values[positions]

    return external_values


def convert_external_derivative_to_internal(external_derivative):
    pass

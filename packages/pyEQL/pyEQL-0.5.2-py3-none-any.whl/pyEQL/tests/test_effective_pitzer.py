"""
pyEQL test suite for Effective Pitzer Model
===========================================

This file contains tests for the Effective Pitzer Model
implemented in pyEQL.

The Effective Pitzer Model is described in Mistry et al.
(DOI: 10.1016/j.desal.2013.03.015). The paper validates
the model by showing the calculated activity coefficients
for each component of synthetic seawater (composition
given in Table 2 of the paper). The mock seawater
has a mass ratio of NaCl:MgCl2:Na2SO4:CaCl2:KCl
of 24.53:5.20:4.09:1.16:0.695, and the total
salinity is varied.

        MW	    g/L	    mol/L
NaCl	58.44	24.53	0.419746749
MgCl2	95.2	5.2	    0.054621849
Na2SO4	142	    4.09	0.028802817
CaCl2	110.98	1.16	0.010452334
KCl	    74.55	0.0695	0.00093226

The total molality is 0.515 mol salts/kg

This test suite replicates that synthetic seawter and then
confirms that pyEQL's output of activity and fugacity
coefficients matches that given by the authors.

pyEQL probably uses different pitzer parameters than
the paper, so perfect accuracy is not expected.

"""

import pyEQL
import unittest


class Test_effective_pitzer(unittest.TestCase, pyEQL.CustomAssertions):
    """
    test osmotic coefficient based on the Pitzer model
    ------------------------------------------------

    """

    def setUp(self):
        # relative error tolerance for assertWithinExperimentalError
        self.tol = 0.15

    def mock_seawater(self, multiple):
        """
        Create a solution of mock seawater.
        Multiple is a scale factor by which the base
        composition (regular seawater) is scaled.
        """
        s1 = pyEQL.Solution(
            [
                ["Na+", str(multiple * 0.4197 + multiple * 2 * 0.0288) + "mol/L"],
                [
                    "Cl-",
                    str(
                        multiple * 0.4197
                        + multiple * 2 * 0.0546
                        + multiple * 2 * 0.01045
                        + multiple * 0.00093
                    )
                    + "mol/L",
                ],
                ["Mg+2", str(multiple * 0.0546) + "mol/L"],
                ["SO4-2", str(multiple * 0.0288) + "mol/L"],
                ["Ca+2", str(multiple * 0.01045) + "mol/L"],
                ["K+", str(multiple * 0.00093) + "mol/L"],
            ]
        )
        return s1

    def test_effective_pitzer_nacl_activity(self):
        # test the activity coefficient of NaCl
        # corresponds to 0.515m, 1.03m, 2.58m, and 4.1m
        multiple = [1, 2, 5, 8]
        expected = [0.7, 0.7, 0.8, 1.1]

        # import the parameters database
        from pyEQL import paramsDB as db

        for item in range(len(multiple)):
            s1 = self.mock_seawater(multiple[item])
            Salt = pyEQL.salt_ion_match.Salt("Na+", "Cl-")
            db.search_parameters(Salt.formula)
            param = db.get_parameter(Salt.formula, "pitzer_parameters_activity")
            alpha1 = 2
            alpha2 = 0
            molality = Salt.get_effective_molality(s1.get_ionic_strength())
            temperature = str(s1.get_temperature())

            activity_coefficient = pyEQL.activity_correction.get_activity_coefficient_pitzer(
                s1.get_ionic_strength(),
                molality,
                alpha1,
                alpha2,
                param.get_value()[0],
                param.get_value()[1],
                param.get_value()[2],
                param.get_value()[3],
                Salt.z_cation,
                Salt.z_anion,
                Salt.nu_cation,
                Salt.nu_anion,
                temperature,
            )

            # convert the result to a rational activity coefficient
            result = activity_coefficient * (
                1
                + pyEQL.unit("0.018 kg/mol")
                * s1.get_total_moles_solute()
                / s1.get_solvent_mass()
            )
            # print(result,expected[item])
            self.assertWithinExperimentalError(result, expected[item], self.tol)

    def test_effective_pitzer_mgcl2_activity(self):
        # test the activity coefficient of MgCl2
        # corresponds to 0.515m, 1.03m, 2.58m, and 4.1m
        multiple = [1, 2, 5, 8]
        expected = [0.5, 0.5, 0.67, 1.15]

        # import the parameters database
        from pyEQL import paramsDB as db

        for item in range(len(multiple)):
            s1 = self.mock_seawater(multiple[item])
            Salt = pyEQL.salt_ion_match.Salt("Mg+2", "Cl-")
            db.search_parameters(Salt.formula)
            param = db.get_parameter(Salt.formula, "pitzer_parameters_activity")
            alpha1 = 2
            alpha2 = 0
            molality = Salt.get_effective_molality(s1.get_ionic_strength())
            temperature = str(s1.get_temperature())

            activity_coefficient = pyEQL.activity_correction.get_activity_coefficient_pitzer(
                s1.get_ionic_strength(),
                molality,
                alpha1,
                alpha2,
                param.get_value()[0],
                param.get_value()[1],
                param.get_value()[2],
                param.get_value()[3],
                Salt.z_cation,
                Salt.z_anion,
                Salt.nu_cation,
                Salt.nu_anion,
                temperature,
            )

            # convert the result to a rational activity coefficient
            result = activity_coefficient * (
                1
                + pyEQL.unit("0.018 kg/mol")
                * s1.get_total_moles_solute()
                / s1.get_solvent_mass()
            )
            # print(result,expected[item])
            self.assertWithinExperimentalError(result, expected[item], self.tol)

    def test_effective_pitzer_KCl_activity(self):
        # test the activity coefficient of KCl
        # corresponds to 0.515m, 1.03m, 2.58m, and 4.1m
        multiple = [1, 2, 5, 8]
        expected = [0.65, 0.61, 0.65, 0.7]

        # import the parameters database
        from pyEQL import paramsDB as db

        for item in range(len(multiple)):
            s1 = self.mock_seawater(multiple[item])
            Salt = pyEQL.salt_ion_match.Salt("K+", "Cl-")
            db.search_parameters(Salt.formula)
            param = db.get_parameter(Salt.formula, "pitzer_parameters_activity")
            alpha1 = 2
            alpha2 = 0
            molality = Salt.get_effective_molality(s1.get_ionic_strength())
            temperature = str(s1.get_temperature())

            activity_coefficient = pyEQL.activity_correction.get_activity_coefficient_pitzer(
                s1.get_ionic_strength(),
                molality,
                alpha1,
                alpha2,
                param.get_value()[0],
                param.get_value()[1],
                param.get_value()[2],
                param.get_value()[3],
                Salt.z_cation,
                Salt.z_anion,
                Salt.nu_cation,
                Salt.nu_anion,
                temperature,
            )

            # convert the result to a rational activity coefficient
            result = activity_coefficient * (
                1
                + pyEQL.unit("0.018 kg/mol")
                * s1.get_total_moles_solute()
                / s1.get_solvent_mass()
            )
            # print(result,expected[item])
            self.assertWithinExperimentalError(result, expected[item], self.tol)

    @unittest.expectedFailure
    def test_effective_pitzer_na2so4_activity(self):
        # test the activity coefficient of Na2SO4
        # corresponds to 0.515m, 1.03m, 2.58m, and 4.1m
        multiple = [1, 2, 5, 8]
        expected = [0.38, 0.3, 0.25, 0.2]

        # import the parameters database
        from pyEQL import paramsDB as db

        for item in range(len(multiple)):
            s1 = self.mock_seawater(multiple[item])
            Salt = pyEQL.salt_ion_match.Salt("Na+", "SO4-2")
            db.search_parameters(Salt.formula)
            param = db.get_parameter(Salt.formula, "pitzer_parameters_activity")
            alpha1 = 2
            alpha2 = 0
            molality = Salt.get_effective_molality(s1.get_ionic_strength())
            temperature = str(s1.get_temperature())

            activity_coefficient = pyEQL.activity_correction.get_activity_coefficient_pitzer(
                s1.get_ionic_strength(),
                molality,
                alpha1,
                alpha2,
                param.get_value()[0],
                param.get_value()[1],
                param.get_value()[2],
                param.get_value()[3],
                Salt.z_cation,
                Salt.z_anion,
                Salt.nu_cation,
                Salt.nu_anion,
                temperature,
            )

            # convert the result to a rational activity coefficient
            result = activity_coefficient * (
                1
                + pyEQL.unit("0.018 kg/mol")
                * s1.get_total_moles_solute()
                / s1.get_solvent_mass()
            )
            # print(result,expected[item])
            self.assertWithinExperimentalError(result, expected[item], self.tol)

    def test_effective_pitzer_fugacity(self):
        # test the fugacity coefficient of mock seawater
        # corresponds to 0.515m, 2.58m, 4.1m, and 5.15 m
        multiple = [1, 5, 8, 10]
        expected = [1, 1, 0.95, 0.95]

        # import the parameters database
        from pyEQL import paramsDB as db

        for item in range(len(multiple)):
            s1 = self.mock_seawater(multiple[item])
            result = s1.get_osmotic_coefficient(scale="fugacity")

            # print(result,expected[item])
            self.assertWithinExperimentalError(result, expected[item], self.tol)


if __name__ == "__main__":
    unittest.main()

/*
  Wrappers around the C integration code for planar Orbits
*/
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <bovy_coords.h>
#include <bovy_symplecticode.h>
#include <bovy_rk.h>
#include <leung_dop853.h>
#include <integrateFullOrbit.h>
//Potentials
#include <galpy_potentials.h>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
#ifndef ORBITS_CHUNKSIZE
#define ORBITS_CHUNKSIZE 1
#endif
//Macros to export functions in DLL on different OS
#if defined(_WIN32)
#define EXPORT __declspec(dllexport)
#elif defined(__GNUC__)
#define EXPORT __attribute__((visibility("default")))
#else
// Just do nothing?
#define EXPORT
#endif
/*
  Function Declarations
*/
void evalPlanarRectForce(double, double *, double *,
			 int, struct potentialArg *);
void evalPlanarRectDeriv(double, double *, double *,
			 int, struct potentialArg *);
void evalPlanarRectDeriv_dxdv(double, double *, double *,
			      int, struct potentialArg *);
void initPlanarMovingObjectSplines(struct potentialArg *, double ** pot_args);
/*
  Actual functions
*/
void parse_leapFuncArgs(int npot,struct potentialArg * potentialArgs,
			int ** pot_type,
			double ** pot_args){
  int ii,jj;
  init_potentialArgs(npot,potentialArgs);
  for (ii=0; ii < npot; ii++){
    switch ( *(*pot_type)++ ) {
    case 0: //LogarithmicHaloPotential, 4 arguments
      potentialArgs->potentialEval= &LogarithmicHaloPotentialEval;
      potentialArgs->planarRforce= &LogarithmicHaloPotentialPlanarRforce;
      potentialArgs->planarphiforce= &LogarithmicHaloPotentialPlanarphiforce;
      potentialArgs->planarR2deriv= &LogarithmicHaloPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &LogarithmicHaloPotentialPlanarphi2deriv;
      potentialArgs->planarRphideriv= &LogarithmicHaloPotentialPlanarRphideriv;
      potentialArgs->nargs= 4;
      break;
    case 1: //DehnenBarPotential, 6 arguments
      potentialArgs->planarRforce= &DehnenBarPotentialPlanarRforce;
      potentialArgs->planarphiforce= &DehnenBarPotentialPlanarphiforce;
      potentialArgs->planarR2deriv= &DehnenBarPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &DehnenBarPotentialPlanarphi2deriv;
      potentialArgs->planarRphideriv= &DehnenBarPotentialPlanarRphideriv;
      potentialArgs->nargs= 6;
      break;
    case 2: //TransientLogSpiralPotential, 8 arguments
      potentialArgs->planarRforce= &TransientLogSpiralPotentialRforce;
      potentialArgs->planarphiforce= &TransientLogSpiralPotentialphiforce;
      potentialArgs->nargs= 8;
      break;
    case 3: //SteadyLogSpiralPotential, 8 arguments
      potentialArgs->planarRforce= &SteadyLogSpiralPotentialRforce;
      potentialArgs->planarphiforce= &SteadyLogSpiralPotentialphiforce;
      potentialArgs->nargs= 8;
      break;
    case 4: //EllipticalDiskPotential, 6 arguments
      potentialArgs->planarRforce= &EllipticalDiskPotentialRforce;
      potentialArgs->planarphiforce= &EllipticalDiskPotentialphiforce;
      potentialArgs->planarR2deriv= &EllipticalDiskPotentialR2deriv;
      potentialArgs->planarphi2deriv= &EllipticalDiskPotentialphi2deriv;
      potentialArgs->planarRphideriv= &EllipticalDiskPotentialRphideriv;
      potentialArgs->nargs= 6;
      break;
    case 5: //MiyamotoNagaiPotential, 3 arguments
      potentialArgs->potentialEval= &MiyamotoNagaiPotentialEval;
      potentialArgs->planarRforce= &MiyamotoNagaiPotentialPlanarRforce;
      potentialArgs->planarphiforce= &ZeroPlanarForce;
      potentialArgs->planarR2deriv= &MiyamotoNagaiPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &ZeroPlanarForce;
      potentialArgs->planarRphideriv= &ZeroPlanarForce;
      potentialArgs->nargs= 3;
      break;
    case 6: //LopsidedDiskPotential, 4 arguments
      potentialArgs->planarRforce= &LopsidedDiskPotentialRforce;
      potentialArgs->planarphiforce= &LopsidedDiskPotentialphiforce;
      potentialArgs->planarR2deriv= &LopsidedDiskPotentialR2deriv;
      potentialArgs->planarphi2deriv= &LopsidedDiskPotentialphi2deriv;
      potentialArgs->planarRphideriv= &LopsidedDiskPotentialRphideriv;
      potentialArgs->nargs= 4;
      break;
    case 7: //PowerSphericalPotential, 2 arguments
      potentialArgs->potentialEval= &PowerSphericalPotentialEval;
      potentialArgs->planarRforce= &PowerSphericalPotentialPlanarRforce;
      potentialArgs->planarphiforce= &ZeroPlanarForce;
      potentialArgs->planarR2deriv= &PowerSphericalPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &ZeroPlanarForce;
      potentialArgs->planarRphideriv= &ZeroPlanarForce;
      potentialArgs->nargs= 2;
      break;
    case 8: //HernquistPotential, 2 arguments
      potentialArgs->potentialEval= &HernquistPotentialEval;
      potentialArgs->planarRforce= &HernquistPotentialPlanarRforce;
      potentialArgs->planarphiforce= &ZeroPlanarForce;
      potentialArgs->planarR2deriv= &HernquistPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &ZeroPlanarForce;
      potentialArgs->planarRphideriv= &ZeroPlanarForce;
      potentialArgs->nargs= 2;
      break;
    case 9: //NFWPotential, 2 arguments
      potentialArgs->potentialEval= &NFWPotentialEval;
      potentialArgs->planarRforce= &NFWPotentialPlanarRforce;
      potentialArgs->planarphiforce= &ZeroPlanarForce;
      potentialArgs->planarR2deriv= &NFWPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &ZeroPlanarForce;
      potentialArgs->planarRphideriv= &ZeroPlanarForce;
      potentialArgs->nargs= 2;
      break;
    case 10: //JaffePotential, 2 arguments
      potentialArgs->potentialEval= &JaffePotentialEval;
      potentialArgs->planarRforce= &JaffePotentialPlanarRforce;
      potentialArgs->planarphiforce= &ZeroPlanarForce;
      potentialArgs->planarR2deriv= &JaffePotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &ZeroPlanarForce;
      potentialArgs->planarRphideriv= &ZeroPlanarForce;
      potentialArgs->nargs= 2;
      break;
    case 11: //DoubleExponentialDiskPotential, XX arguments
      potentialArgs->potentialEval= &DoubleExponentialDiskPotentialEval;
      potentialArgs->planarRforce= &DoubleExponentialDiskPotentialPlanarRforce;
      potentialArgs->planarphiforce= &ZeroPlanarForce;
      //potentialArgs->planarR2deriv= &DoubleExponentialDiskPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &ZeroPlanarForce;
      potentialArgs->planarRphideriv= &ZeroPlanarForce;
      //Look at pot_args to figure out the number of arguments
      potentialArgs->nargs= (int) (8 + 2 * *(*pot_args+5) + 4 * ( *(*pot_args+4) + 1 ));
      break;
    case 12: //FlattenedPowerPotential, 4 arguments
      potentialArgs->potentialEval= &FlattenedPowerPotentialEval;
      potentialArgs->planarRforce= &FlattenedPowerPotentialPlanarRforce;
      potentialArgs->planarphiforce= &ZeroPlanarForce;
      potentialArgs->planarR2deriv= &FlattenedPowerPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &ZeroPlanarForce;
      potentialArgs->planarRphideriv= &ZeroPlanarForce;
      potentialArgs->nargs= 3;
      break;
    case 14: //IsochronePotential, 2 arguments
      potentialArgs->potentialEval= &IsochronePotentialEval;
      potentialArgs->planarRforce= &IsochronePotentialPlanarRforce;
      potentialArgs->planarphiforce= &ZeroPlanarForce;
      potentialArgs->planarR2deriv= &IsochronePotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &ZeroPlanarForce;
      potentialArgs->planarRphideriv= &ZeroPlanarForce;
      potentialArgs->nargs= 2;
      break;
    case 15: //PowerSphericalPotentialwCutoff, 3 arguments
      potentialArgs->potentialEval= &PowerSphericalPotentialwCutoffEval;
      potentialArgs->planarRforce= &PowerSphericalPotentialwCutoffPlanarRforce;
      potentialArgs->planarphiforce= &ZeroPlanarForce;
      potentialArgs->planarR2deriv= &PowerSphericalPotentialwCutoffPlanarR2deriv;
      potentialArgs->planarphi2deriv= &ZeroPlanarForce;
      potentialArgs->planarRphideriv= &ZeroPlanarForce;
      potentialArgs->nargs= 3;
      break;
    case 16: //KuzminKutuzovStaeckelPotential, 3 arguments
      potentialArgs->potentialEval= &KuzminKutuzovStaeckelPotentialEval;
      potentialArgs->planarRforce= &KuzminKutuzovStaeckelPotentialPlanarRforce;
      potentialArgs->planarphiforce= &ZeroPlanarForce;
      potentialArgs->planarR2deriv= &KuzminKutuzovStaeckelPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &ZeroPlanarForce;
      potentialArgs->planarRphideriv= &ZeroPlanarForce;
      potentialArgs->nargs= 3;
      break;
    case 17: //PlummerPotential, 2 arguments
      potentialArgs->potentialEval= &PlummerPotentialEval;
      potentialArgs->planarRforce= &PlummerPotentialPlanarRforce;
      potentialArgs->planarphiforce= &ZeroPlanarForce;
      potentialArgs->planarR2deriv= &PlummerPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &ZeroPlanarForce;
      potentialArgs->planarRphideriv= &ZeroPlanarForce;
      potentialArgs->nargs= 2;
      break;
    case 18: //PseudoIsothermalPotential, 2 arguments
      potentialArgs->potentialEval= &PseudoIsothermalPotentialEval;
      potentialArgs->planarRforce= &PseudoIsothermalPotentialPlanarRforce;
      potentialArgs->planarphiforce= &ZeroPlanarForce;
      potentialArgs->planarR2deriv= &PseudoIsothermalPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &ZeroPlanarForce;
      potentialArgs->planarRphideriv= &ZeroPlanarForce;
      potentialArgs->nargs= 2;
      break;
    case 19: //KuzminDiskPotential, 2 arguments
      potentialArgs->potentialEval= &KuzminDiskPotentialEval;
      potentialArgs->planarRforce= &KuzminDiskPotentialPlanarRforce;
      potentialArgs->planarphiforce= &ZeroPlanarForce;
      potentialArgs->planarR2deriv= &KuzminDiskPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &ZeroPlanarForce;
      potentialArgs->planarRphideriv= &ZeroPlanarForce;
      potentialArgs->nargs= 2;
      break;
    case 20: //BurkertPotential, 2 arguments
      potentialArgs->potentialEval= &BurkertPotentialEval;
      potentialArgs->planarRforce= &BurkertPotentialPlanarRforce;
      potentialArgs->planarphiforce= &ZeroPlanarForce;
      potentialArgs->planarR2deriv= &BurkertPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &ZeroPlanarForce;
      potentialArgs->planarRphideriv= &ZeroPlanarForce;
      potentialArgs->nargs= 2;
      break;
    case 21: // TriaxialHernquistPotential, lots of arguments
      potentialArgs->planarRforce = &EllipsoidalPotentialPlanarRforce;
      potentialArgs->planarphiforce = &EllipsoidalPotentialPlanarphiforce;
      //potentialArgs->planarR2deriv = &EllipsoidalPotentialPlanarR2deriv;
      //potentialArgs->planarphi2deriv = &EllipsoidalPotentialPlanarphi2deriv;
      //potentialArgs->planarRphideriv = &EllipsoidalPotentialPlanarRphideriv;
      // Also assign functions specific to EllipsoidalPotential
      potentialArgs->psi= &TriaxialHernquistPotentialpsi;
      potentialArgs->mdens= &TriaxialHernquistPotentialmdens;
      potentialArgs->mdensDeriv= &TriaxialHernquistPotentialmdensDeriv;
      potentialArgs->nargs = (int) (21 + *(*pot_args+7) + 2 * *(*pot_args 
					    + (int) (*(*pot_args+7) + 20)));
      break;    
    case 22: // TriaxialNFWPotential, lots of arguments
      potentialArgs->planarRforce = &EllipsoidalPotentialPlanarRforce;
      potentialArgs->planarphiforce = &EllipsoidalPotentialPlanarphiforce;
      //potentialArgs->planarR2deriv = &EllipsoidalPotentialPlanarR2deriv;
      //potentialArgs->planarphi2deriv = &EllipsoidalPotentialPlanarphi2deriv;
      //potentialArgs->planarRphideriv = &EllipsoidalPotentialPlanarRphideriv;
      // Also assign functions specific to EllipsoidalPotential
      potentialArgs->psi= &TriaxialNFWPotentialpsi;
      potentialArgs->mdens= &TriaxialNFWPotentialmdens;
      potentialArgs->mdensDeriv= &TriaxialNFWPotentialmdensDeriv;
      potentialArgs->nargs = (int) (21 + *(*pot_args+7) + 2 * *(*pot_args 
					    + (int) (*(*pot_args+7) + 20)));
      break;    
    case 23: // TriaxialJaffePotential, lots of arguments
      potentialArgs->planarRforce = &EllipsoidalPotentialPlanarRforce;
      potentialArgs->planarphiforce = &EllipsoidalPotentialPlanarphiforce;
      //potentialArgs->planarR2deriv = &EllipsoidalPotentialPlanarR2deriv;
      //potentialArgs->planarphi2deriv = &EllipsoidalPotentialPlanarphi2deriv;
      //potentialArgs->planarRphideriv = &EllipsoidalPotentialPlanarRphideriv;
      // Also assign functions specific to EllipsoidalPotential
      potentialArgs->psi= &TriaxialJaffePotentialpsi;
      potentialArgs->mdens= &TriaxialJaffePotentialmdens;
      potentialArgs->mdensDeriv= &TriaxialJaffePotentialmdensDeriv;
      potentialArgs->nargs = (int) (21 + *(*pot_args+7) + 2 * *(*pot_args 
					    + (int) (*(*pot_args+7) + 20)));
      break;    
    case 24: //SCFPotential, many arguments
      potentialArgs->potentialEval= &SCFPotentialEval;
      potentialArgs->planarRforce= &SCFPotentialPlanarRforce;
      potentialArgs->planarphiforce= &SCFPotentialPlanarphiforce;
      potentialArgs->planarR2deriv= &SCFPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &SCFPotentialPlanarphi2deriv;
      potentialArgs->planarRphideriv= &SCFPotentialPlanarRphideriv;
      potentialArgs->nargs= (int) (5 + (1 + *(*pot_args + 1)) * *(*pot_args+2) * *(*pot_args+3)* *(*pot_args+4) + 7);
      break;
    case 25: //SoftenedNeedleBarPotential, 13 arguments
      potentialArgs->potentialEval= &SoftenedNeedleBarPotentialEval;
      potentialArgs->planarRforce= &SoftenedNeedleBarPotentialPlanarRforce;
      potentialArgs->planarphiforce= &SoftenedNeedleBarPotentialPlanarphiforce;
      potentialArgs->nargs= (int) 13;
      break;    
    case 26: //DiskSCFPotential, nsigma+3 arguments
      potentialArgs->potentialEval= &DiskSCFPotentialEval;
      potentialArgs->planarRforce= &DiskSCFPotentialPlanarRforce;
      potentialArgs->planarphiforce= &ZeroPlanarForce;
      potentialArgs->nargs= (int) **pot_args + 3;
      break;
    case 27: // SpiralArmsPotential, 10 arguments + array of Cs
      potentialArgs->planarRforce = &SpiralArmsPotentialPlanarRforce;
      potentialArgs->planarphiforce = &SpiralArmsPotentialPlanarphiforce;
      potentialArgs->planarR2deriv = &SpiralArmsPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv = &SpiralArmsPotentialPlanarphi2deriv;
      potentialArgs->planarRphideriv = &SpiralArmsPotentialPlanarRphideriv;
      potentialArgs->nargs = (int) 10 + **pot_args;
      break;
    case 28: //CosmphiDiskPotential, 9 arguments
      potentialArgs->planarRforce= &CosmphiDiskPotentialRforce;
      potentialArgs->planarphiforce= &CosmphiDiskPotentialphiforce;
      potentialArgs->planarR2deriv= &CosmphiDiskPotentialR2deriv;
      potentialArgs->planarphi2deriv= &CosmphiDiskPotentialphi2deriv;
      potentialArgs->planarRphideriv= &CosmphiDiskPotentialRphideriv;
      potentialArgs->nargs= 9;
      break;
    case 29: //HenonHeilesPotential, 1 argument
      potentialArgs->planarRforce= &HenonHeilesPotentialRforce;
      potentialArgs->planarphiforce= &HenonHeilesPotentialphiforce;
      potentialArgs->planarR2deriv= &HenonHeilesPotentialR2deriv;
      potentialArgs->planarphi2deriv= &HenonHeilesPotentialphi2deriv;
      potentialArgs->planarRphideriv= &HenonHeilesPotentialRphideriv;
      potentialArgs->nargs= 1;
      break;
    case 30: // PerfectEllipsoidPotential, lots of arguments
      potentialArgs->planarRforce = &EllipsoidalPotentialPlanarRforce;
      potentialArgs->planarphiforce = &EllipsoidalPotentialPlanarphiforce;
      //potentialArgs->planarR2deriv = &EllipsoidalPotentialPlanarR2deriv;
      //potentialArgs->planarphi2deriv = &EllipsoidalPotentialPlanarphi2deriv;
      //potentialArgs->planarRphideriv = &EllipsoidalPotentialPlanarRphideriv;
      // Also assign functions specific to EllipsoidalPotential
      potentialArgs->psi= &PerfectEllipsoidPotentialpsi;
      potentialArgs->mdens= &PerfectEllipsoidPotentialmdens;
      potentialArgs->mdensDeriv= &PerfectEllipsoidPotentialmdensDeriv;
      potentialArgs->nargs = (int) (21 + *(*pot_args+7) + 2 * *(*pot_args 
					    + (int) (*(*pot_args+7) + 20)));
      break;
    // 31: KGPotential
    // 32: IsothermalDiskPotential
    case 33: //DehnenCoreSphericalpotential
      potentialArgs->potentialEval= &DehnenCoreSphericalPotentialEval;
      potentialArgs->planarRforce= &DehnenCoreSphericalPotentialPlanarRforce;
      potentialArgs->planarphiforce= &ZeroPlanarForce;
      potentialArgs->planarR2deriv= &DehnenCoreSphericalPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &ZeroPlanarForce;
      potentialArgs->planarRphideriv= &ZeroPlanarForce;
      potentialArgs->nargs= 2;
      break;
    case 34: //DehnenSphericalpotential
      potentialArgs->potentialEval= &DehnenSphericalPotentialEval;
      potentialArgs->planarRforce= &DehnenSphericalPotentialPlanarRforce;
      potentialArgs->planarphiforce= &ZeroPlanarForce;
      potentialArgs->planarR2deriv= &DehnenSphericalPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &ZeroPlanarForce;
      potentialArgs->planarRphideriv= &ZeroPlanarForce;
      potentialArgs->nargs= 3;
      break;
    case 35: //HomogeneousSpherePotential, 3 arguments
      potentialArgs->potentialEval= &HomogeneousSpherePotentialEval;
      potentialArgs->planarRforce= &HomogeneousSpherePotentialPlanarRforce;
      potentialArgs->planarphiforce= &ZeroPlanarForce;
      potentialArgs->planarR2deriv= &HomogeneousSpherePotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &ZeroPlanarForce;
      potentialArgs->planarRphideriv= &ZeroPlanarForce;
      potentialArgs->nargs= 3;
      break;
//////////////////////////////// WRAPPERS /////////////////////////////////////
    case -1: //DehnenSmoothWrapperPotential
      potentialArgs->potentialEval= &DehnenSmoothWrapperPotentialEval;
      potentialArgs->planarRforce= &DehnenSmoothWrapperPotentialPlanarRforce;
      potentialArgs->planarphiforce= &DehnenSmoothWrapperPotentialPlanarphiforce;
      potentialArgs->planarR2deriv= &DehnenSmoothWrapperPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &DehnenSmoothWrapperPotentialPlanarphi2deriv;
      potentialArgs->planarRphideriv= &DehnenSmoothWrapperPotentialPlanarRphideriv;
      potentialArgs->nargs= (int) 4;
      break;
    case -2: //SolidBodyRotationWrapperPotential
      potentialArgs->planarRforce= &SolidBodyRotationWrapperPotentialPlanarRforce;
      potentialArgs->planarphiforce= &SolidBodyRotationWrapperPotentialPlanarphiforce;
      potentialArgs->planarR2deriv= &SolidBodyRotationWrapperPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &SolidBodyRotationWrapperPotentialPlanarphi2deriv;
      potentialArgs->planarRphideriv= &SolidBodyRotationWrapperPotentialPlanarRphideriv;
      potentialArgs->nargs= (int) 3;
      break;
    case -4: //CorotatingRotationWrapperPotential
      potentialArgs->planarRforce= &CorotatingRotationWrapperPotentialPlanarRforce;
      potentialArgs->planarphiforce= &CorotatingRotationWrapperPotentialPlanarphiforce;
      potentialArgs->planarR2deriv= &CorotatingRotationWrapperPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &CorotatingRotationWrapperPotentialPlanarphi2deriv;
      potentialArgs->planarRphideriv= &CorotatingRotationWrapperPotentialPlanarRphideriv;
      potentialArgs->nargs= (int) 5;
      break;
    case -5: //GaussianAmplitudeWrapperPotential
      potentialArgs->planarRforce= &GaussianAmplitudeWrapperPotentialPlanarRforce;
      potentialArgs->planarphiforce= &GaussianAmplitudeWrapperPotentialPlanarphiforce;
      potentialArgs->planarR2deriv= &GaussianAmplitudeWrapperPotentialPlanarR2deriv;
      potentialArgs->planarphi2deriv= &GaussianAmplitudeWrapperPotentialPlanarphi2deriv;
      potentialArgs->planarRphideriv= &GaussianAmplitudeWrapperPotentialPlanarRphideriv;
      potentialArgs->nargs= (int) 3;
      break;
    case -6: //MovingObjectPotential
      potentialArgs->planarRforce= &MovingObjectPotentialPlanarRforce;
      potentialArgs->planarphiforce= &MovingObjectPotentialPlanarphiforce;
      potentialArgs->nargs= (int) 3;
      break;
    }
    int setupSplines = *(*pot_type-1) == -6 ? 1 : 0;
    if ( *(*pot_type-1) < 0) { // Parse wrapped potential for wrappers
      potentialArgs->nwrapped= (int) *(*pot_args)++;
      potentialArgs->wrappedPotentialArg= \
	(struct potentialArg *) malloc ( potentialArgs->nwrapped	\
					 * sizeof (struct potentialArg) );
      parse_leapFuncArgs(potentialArgs->nwrapped,
			 potentialArgs->wrappedPotentialArg,
			 pot_type,pot_args);
    }
    if (setupSplines) initPlanarMovingObjectSplines(potentialArgs, pot_args);
    potentialArgs->args= (double *) malloc( potentialArgs->nargs * sizeof(double));
    for (jj=0; jj < potentialArgs->nargs; jj++){
      *(potentialArgs->args)= *(*pot_args)++;
      potentialArgs->args++;
    }
    potentialArgs->args-= potentialArgs->nargs;
    potentialArgs++;
  }
  potentialArgs-= npot;
}
EXPORT void integratePlanarOrbit(int nobj,
				 double *yo,
				 int nt, 
				 double *t,
				 int npot,
				 int * pot_type,
				 double * pot_args,
				 double dt,
				 double rtol,
				 double atol,
				 double *result,
				 int * err,
				 int odeint_type){
  //Set up the forces, first count
  int ii,jj;
  int dim;
  int max_threads;
  int * thread_pot_type;
  double * thread_pot_args;
  max_threads= ( nobj < omp_get_max_threads() ) ? nobj : omp_get_max_threads();
  // Because potentialArgs may cache, safest to have one / thread
  struct potentialArg * potentialArgs= (struct potentialArg *) malloc ( max_threads * npot * sizeof (struct potentialArg) );
#pragma omp parallel for schedule(static,1) private(ii,thread_pot_type,thread_pot_args) num_threads(max_threads) 
  for (ii=0; ii < max_threads; ii++) {
    thread_pot_type= pot_type; // need to make thread-private pointers, bc
    thread_pot_args= pot_args; // these pointers are changed in parse_...
    parse_leapFuncArgs(npot,potentialArgs+ii*npot,
      &thread_pot_type,&thread_pot_args);
  }
  //Integrate
  void (*odeint_func)(void (*func)(double, double *, double *,
			   int, struct potentialArg *),
		      int,
		      double *,
		      int, double, double *,
		      int, struct potentialArg *,
		      double, double,
		      double *,int *);
  void (*odeint_deriv_func)(double, double *, double *,
			    int,struct potentialArg *);
  switch ( odeint_type ) {
  case 0: //leapfrog
    odeint_func= &leapfrog;
    odeint_deriv_func= &evalPlanarRectForce;
    dim= 2;
    break;
  case 1: //RK4
    odeint_func= &bovy_rk4;
    odeint_deriv_func= &evalPlanarRectDeriv;
    dim= 4;
    break;
  case 2: //RK6
    odeint_func= &bovy_rk6;
    odeint_deriv_func= &evalPlanarRectDeriv;
    dim= 4;
    break;
  case 3: //symplec4
    odeint_func= &symplec4;
    odeint_deriv_func= &evalPlanarRectForce;
    dim= 2;
    break;
  case 4: //symplec6
    odeint_func= &symplec6;
    odeint_deriv_func= &evalPlanarRectForce;
    dim= 2;
    break;
  case 5: //DOPR54
    odeint_func= &bovy_dopr54;
    odeint_deriv_func= &evalPlanarRectDeriv;
    dim= 4;
    break;
  case 6: //DOP853
    odeint_func= &dop853;
    odeint_deriv_func= &evalPlanarRectDeriv;
    dim= 4;
    break;
  }
#pragma omp parallel for schedule(dynamic,ORBITS_CHUNKSIZE) private(ii,jj) num_threads(max_threads)
  for (ii=0; ii < nobj; ii++) {
    polar_to_rect_galpy(yo+4*ii);
    odeint_func(odeint_deriv_func,dim,yo+4*ii,nt,dt,t,
		npot,potentialArgs+omp_get_thread_num()*npot,rtol,atol,
		result+4*nt*ii,err+ii);
    for (jj= 0; jj < nt; jj++)
      rect_to_polar_galpy(result+4*jj+4*nt*ii);
  }
  //Free allocated memory
#pragma omp parallel for schedule(static,1) private(ii) num_threads(max_threads)
  for (ii=0; ii < max_threads; ii++)
    free_potentialArgs(npot,potentialArgs+ii*npot);
  free(potentialArgs);
  //Done!
}

EXPORT void integratePlanarOrbit_dxdv(double *yo,
				      int nt, 
				      double *t,
				      int npot,
				      int * pot_type,
				      double * pot_args,
				      double dt,
				      double rtol,
				      double atol,
				      double *result,
				      int * err,
				      int odeint_type){
  //Set up the forces, first count
  int dim;
  struct potentialArg * potentialArgs= (struct potentialArg *) malloc ( npot * sizeof (struct potentialArg) );
  parse_leapFuncArgs(npot,potentialArgs,&pot_type,&pot_args);
  //Integrate
  void (*odeint_func)(void (*func)(double, double *, double *,
			   int, struct potentialArg *),
		      int,
		      double *,
		      int, double, double *,
		      int, struct potentialArg *,
		      double, double,
		      double *,int *);
  void (*odeint_deriv_func)(double, double *, double *,
			    int,struct potentialArg *);
  switch ( odeint_type ) {
  case 1: //RK4
    odeint_func= &bovy_rk4;
    odeint_deriv_func= &evalPlanarRectDeriv_dxdv;
    dim= 8;
    break;
  case 2: //RK6
    odeint_func= &bovy_rk6;
    odeint_deriv_func= &evalPlanarRectDeriv_dxdv;
    dim= 8;
    break;
  case 5: //DOPR54
    odeint_func= &bovy_dopr54;
    odeint_deriv_func= &evalPlanarRectDeriv_dxdv;
    dim= 8;
    break;
  case 6: //DOP853
    odeint_func= &dop853;
    odeint_deriv_func= &evalPlanarRectDeriv_dxdv;
    dim= 8;
    break;
  }
  odeint_func(odeint_deriv_func,dim,yo,nt,dt,t,npot,potentialArgs,rtol,atol,
	      result,err);
  //Free allocated memory
  free_potentialArgs(npot,potentialArgs);
  free(potentialArgs);
  //Done!
}

void evalPlanarRectForce(double t, double *q, double *a,
			 int nargs, struct potentialArg * potentialArgs){
  double sinphi, cosphi, x, y, phi,R,Rforce,phiforce;
  //q is rectangular so calculate R and phi
  x= *q;
  y= *(q+1);
  R= sqrt(x*x+y*y);
  phi= acos(x/R);
  sinphi= y/R;
  cosphi= x/R;
  if ( y < 0. ) phi= 2.*M_PI-phi;
  //Calculate the forces
  Rforce= calcPlanarRforce(R,phi,t,nargs,potentialArgs);
  phiforce= calcPlanarphiforce(R,phi,t,nargs,potentialArgs);
  *a++= cosphi*Rforce-1./R*sinphi*phiforce;
  *a--= sinphi*Rforce+1./R*cosphi*phiforce;
}
void evalPlanarRectDeriv(double t, double *q, double *a,
			 int nargs, struct potentialArg * potentialArgs){
  double sinphi, cosphi, x, y, phi,R,Rforce,phiforce;
  //first two derivatives are just the velocities
  *a++= *(q+2);
  *a++= *(q+3);
  //Rest is force
  //q is rectangular so calculate R and phi
  x= *q;
  y= *(q+1);
  R= sqrt(x*x+y*y);
  phi= acos(x/R);
  sinphi= y/R;
  cosphi= x/R;
  if ( y < 0. ) phi= 2.*M_PI-phi;
  //Calculate the forces
  Rforce= calcPlanarRforce(R,phi,t,nargs,potentialArgs);
  phiforce= calcPlanarphiforce(R,phi,t,nargs,potentialArgs);
  *a++= cosphi*Rforce-1./R*sinphi*phiforce;
  *a= sinphi*Rforce+1./R*cosphi*phiforce;
}

void evalPlanarRectDeriv_dxdv(double t, double *q, double *a,
			      int nargs, struct potentialArg * potentialArgs){
  double sinphi, cosphi, x, y, phi,R,Rforce,phiforce;
  double R2deriv, phi2deriv, Rphideriv, dFxdx, dFxdy, dFydx, dFydy;
  //first two derivatives are just the velocities
  *a++= *(q+2);
  *a++= *(q+3);
  //Rest is force
  //q is rectangular so calculate R and phi
  x= *q;
  y= *(q+1);
  R= sqrt(x*x+y*y);
  phi= acos(x/R);
  sinphi= y/R;
  cosphi= x/R;
  if ( y < 0. ) phi= 2.*M_PI-phi;
  //Calculate the forces
  Rforce= calcPlanarRforce(R,phi,t,nargs,potentialArgs);
  phiforce= calcPlanarphiforce(R,phi,t,nargs,potentialArgs);
  *a++= cosphi*Rforce-1./R*sinphi*phiforce;
  *a++= sinphi*Rforce+1./R*cosphi*phiforce;
  //dx derivatives are just dv
  *a++= *(q+6);
  *a++= *(q+7);
  //for the dv derivatives we need also R2deriv, phi2deriv, and Rphideriv
  R2deriv= calcPlanarR2deriv(R,phi,t,nargs,potentialArgs);
  phi2deriv= calcPlanarphi2deriv(R,phi,t,nargs,potentialArgs);
  Rphideriv= calcPlanarRphideriv(R,phi,t,nargs,potentialArgs);
  //..and dFxdx, dFxdy, dFydx, dFydy
  dFxdx= -cosphi*cosphi*R2deriv
    +2.*cosphi*sinphi/R/R*phiforce
    +sinphi*sinphi/R*Rforce
    +2.*sinphi*cosphi/R*Rphideriv
    -sinphi*sinphi/R/R*phi2deriv;
  dFxdy= -sinphi*cosphi*R2deriv
    +(sinphi*sinphi-cosphi*cosphi)/R/R*phiforce
    -cosphi*sinphi/R*Rforce
    -(cosphi*cosphi-sinphi*sinphi)/R*Rphideriv
    +cosphi*sinphi/R/R*phi2deriv;
  dFydx= -cosphi*sinphi*R2deriv
    +(sinphi*sinphi-cosphi*cosphi)/R/R*phiforce
    +(sinphi*sinphi-cosphi*cosphi)/R*Rphideriv
    -sinphi*cosphi/R*Rforce
    +sinphi*cosphi/R/R*phi2deriv;
  dFydy= -sinphi*sinphi*R2deriv
    -2.*sinphi*cosphi/R/R*phiforce
    -2.*sinphi*cosphi/R*Rphideriv
    +cosphi*cosphi/R*Rforce
    -cosphi*cosphi/R/R*phi2deriv;
  *a++= dFxdx * *(q+4) + dFxdy * *(q+5);
  *a= dFydx * *(q+4) + dFydy * *(q+5);
}

void initPlanarMovingObjectSplines(struct potentialArg * potentialArgs, double ** pot_args){
  gsl_interp_accel *x_accel_ptr = gsl_interp_accel_alloc();
  gsl_interp_accel *y_accel_ptr = gsl_interp_accel_alloc();
  int nPts = (int) **pot_args;

  gsl_spline *x_spline = gsl_spline_alloc(gsl_interp_cspline, nPts);
  gsl_spline *y_spline = gsl_spline_alloc(gsl_interp_cspline, nPts);

  double * t_arr = *pot_args+1;
  double * x_arr = t_arr+1*nPts;
  double * y_arr = t_arr+2*nPts;

  double * t= (double *) malloc ( nPts * sizeof (double) );
  double tf = *(t_arr+3*nPts+2);
  double to = *(t_arr+3*nPts+1);

  int ii;
  for (ii=0; ii < nPts; ii++)
    *(t+ii) = (t_arr[ii]-to)/(tf-to);

  gsl_spline_init(x_spline, t, x_arr, nPts);
  gsl_spline_init(y_spline, t, y_arr, nPts);

  potentialArgs->nspline1d= 2;
  potentialArgs->spline1d= (gsl_spline **) malloc ( 2*sizeof ( gsl_spline *) );
  potentialArgs->acc1d= (gsl_interp_accel **) \
    malloc ( 2 * sizeof ( gsl_interp_accel * ) );
  *potentialArgs->spline1d = x_spline;
  *potentialArgs->acc1d = x_accel_ptr;
  *(potentialArgs->spline1d+1)= y_spline;
  *(potentialArgs->acc1d+1)= y_accel_ptr;

  *pot_args = *pot_args+ (int) (1+3*nPts);
  free(t);
}

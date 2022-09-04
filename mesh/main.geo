Include "foil.geo";
Include "WindTunnel.geo";
Include "parameters.geo";

// Units are multiples of chord.
ce = 101;
Arguments[] = {0, 0, 10};
Call Foil;
MainSailLoop = Results[0];

//ce = 1000;
//Arguments[] = {3, 3, 25};
//Call Foil;
//HeadSailLoop = Results[0];

WindTunnelHeight = 5;
WindTunnelLength = 5;
WindTunnelLc = 0.2;
Call WindTunnel;
//
Plane Surface(ce++) = {WindTunnelLoop, MainSailLoop}; //, HeadSailLoop};
TwoDimSurf = ce - 1;

cellDepth = 0.1;

ids[] = Extrude {0, 0, cellDepth}
{
	Surface{TwoDimSurf};
	Layers{1};
	Recombine;
};


Physical Surface("outlet") = {ids[2]};
Physical Surface("walls") = {ids[{3, 5}]};
Physical Surface("inlet") = {ids[4]};
Physical Surface("airfoil") = {ids[{6,7}]};
Physical Surface("frontAndBack") = {ids[0], TwoDimSurf};
Physical Volume("volume") = {ids[1]};

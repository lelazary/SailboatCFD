Macro RotatePoint
    pointId = Arguments[0];
    angle = Arguments[1];
    center[] = Arguments[{2:4}];
    //Rotate {{0, 0, 1.0}, {center[0], center[1], center[2]}, angle}
    Rotate {{0, 0, 1.0}, {0,0,0}, -30 * Pi/180}
    {
        Point{pointId};
    }
Return

Macro RotateAirfoilPoint
    // rotates pointId about quarter-chord.
    Arguments[1] *= -1.0;
    Arguments[{2:4}] = {0 , 0, 0};
    Call RotatePoint;
Return

Macro TranslatePoint
    pointId = Arguments[0];
    dx = Arguments[1];
    dy = Arguments[2];
    Translate {dx, dy, 0}
    {
        Point{pointId};
    }
Return



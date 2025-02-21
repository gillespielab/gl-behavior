% PROGRAM NAME: Reward Well Testing
% AUTHOR: VS
% DESCRIPTION:  toggle the white LED when the IR beam is broken

% initialize
portout[1] = 0
portout[2] = 0
portout[3] = 0
portout[4] = 0
portout[5] = 0
portout[6] = 0
portout[7] = 0
portout[8] = 0
portout[9] = 0
portout[10] = 0
portout[11] = 0
portout[12] = 0
portout[13] = 0
portout[14] = 0
portout[15] = 0
portout[16] = 0

% define the callbacks
callback portin[1] up
	portout[1] = flip
	disp('beam break detected')
end;

callback portin[2] up
	portout[2] = flip
	disp('beam break detected')
end;

callback portin[3] up
	portout[3] = flip
	disp('beam break detected')
end;

callback portin[4] up
	portout[4] = flip
	disp('beam break detected')
end;

callback portin[5] up
	portout[5] = flip
	disp('beam break detected')
end;

callback portin[6] up
	portout[6] = flip
	disp('beam break detected')
end;

callback portin[7] up
	portout[7] = flip
	disp('beam break detected')
end;

callback portin[8] up
	portout[8] = flip
	disp('beam break detected')
end;

callback portin[9] up
	portout[9] = flip
	disp('beam break detected')
end;

callback portin[10] up
	portout[10] = flip
	disp('beam break detected')
end;

callback portin[11] up
	portout[11] = flip
	disp('beam break detected')
end;

callback portin[11] up
	portout[11] = flip
	disp('beam break detected')
end;

callback portin[12] up
	portout[12] = flip
	disp('beam break detected')
end;

callback portin[13] up
	portout[13] = flip
	disp('beam break detected')
end;

callback portin[14] up
	portout[14] = flip
	disp('beam break detected')
end;

callback portin[15] up
	portout[15] = flip
	disp('beam break detected')
end;

callback portin[16] up
	portout[16] = flip
	disp('beam break detected')
end;


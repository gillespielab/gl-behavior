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


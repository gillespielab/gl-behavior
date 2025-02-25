% PROGRAM NAME: 	Linear track with lights
% AUTHOR: 		AKG 
% DESCRIPTION:	alternate between ends, active trial lights up
%	
% PARAMETERS FOR 150uL REWARD
int deliverPeriod= 10   	% pulse duration for peristaltic
int interval = 20		% pulse+interpulse interval
int pulsenum = 7		% # pulses


% set variables for each lane
% each lane has its own reward function and disp

int Lane1_Pump = 0
int Lane1_currWell = 0
int Lane1_lastWell = 0
int Lane1_rewCount = 0
int Lane1_trainCounter = 0
int Lane2_Pump = 0
int Lane2_currWell = 0
int Lane2_lastWell = 0
int Lane2_rewCount = 0
int Lane2_trainCounter = 0
int Lane3_Pump = 0
int Lane3_currWell = 0
int Lane3_lastWell = 0
int Lane3_rewCount = 0
int Lane3_trainCounter = 0
int Lane4_Pump = 0
int Lane4_currWell = 0
int Lane4_lastWell = 0
int Lane4_rewCount = 0
int Lane4_trainCounter = 0

portout[1]=1
portout[2]=1
portout[3]=1
portout[4]=1
portout[5]=1
portout[6]=1
portout[7]=1
portout[8]=1;

function 5
	disp(Lane1_rewCount)
	disp(Lane2_rewCount)
	disp(Lane3_rewCount)
	disp(Lane4_rewCount)
end;

function 1	% lane 1
	Lane1_trainCounter = 0
	while Lane1_trainCounter < pulsenum do every interval 
		portout[Lane1_Pump]=1 % reward
		do in deliverPeriod 
			portout[Lane1_Pump]=0 % reset reward
		end
	Lane1_trainCounter = Lane1_trainCounter + 1
	end 
	Lane1_rewCount = Lane1_rewCount+1
	trigger(5)
end;

function 2	% lane 2
	Lane2_trainCounter = 0
	while Lane2_trainCounter < pulsenum do every interval 
		portout[Lane2_Pump]=1 % reward
		do in deliverPeriod 
			portout[Lane2_Pump]=0 % reset reward
		end
	Lane2_trainCounter = Lane2_trainCounter + 1
	end 
	Lane2_rewCount = Lane2_rewCount+1
	trigger(5)
end;

function 3	 % lane 3
	Lane3_trainCounter = 0
	while Lane3_trainCounter < pulsenum do every interval 
		portout[Lane3_Pump]=1 % reward
		do in deliverPeriod 
			portout[Lane3_Pump]=0 % reset reward
		end
	Lane3_trainCounter = Lane3_trainCounter + 1
	end 
	Lane3_rewCount = Lane3_rewCount+1
	trigger(5)
end;
function 4	% lane 4
	Lane4_trainCounter = 0
	while Lane4_trainCounter < pulsenum do every interval 
		portout[Lane4_Pump]=1 % reward
		do in deliverPeriod 
			portout[Lane4_Pump]=0 % reset reward
		end
	Lane4_trainCounter = Lane4_trainCounter + 1
	end 
	Lane4_rewCount = Lane4_rewCount+1
	trigger(5)	
end;


					
callback portin[1] up   % lane 1A
	Lane1_currWell = 1
	if Lane1_lastWell != Lane1_currWell do
		Lane1_Pump = Lane1_currWell+8
		trigger(1)
		Lane1_lastWell = Lane1_currWell
		portout[1]=0
		portout[2]=1
	end
end;

callback portin[2] up   % lane 1B	
	Lane1_currWell = 2
	if Lane1_lastWell != Lane1_currWell do
		Lane1_Pump = Lane1_currWell + 8
		trigger(1)
		Lane1_lastWell = Lane1_currWell
		portout[2]=0
		portout[1]=1
	end
end;

callback portin[3] up   % lane 2A
	Lane2_currWell = 3
	if Lane2_lastWell != Lane2_currWell do
		Lane2_Pump = Lane2_currWell+8
		trigger(2)
		Lane2_lastWell = Lane2_currWell
		portout[3]=0
		portout[4]=1
	end
end;

callback portin[4] up   % lane 2B	
	Lane2_currWell = 4
	if Lane2_lastWell != Lane2_currWell do
		Lane2_Pump = Lane2_currWell + 8
		trigger(2)
		Lane2_lastWell = Lane2_currWell
		portout[4]=0
		portout[3]=1
	end
end;

callback portin[5] up   % lane 3A
	Lane3_currWell = 5
	if Lane3_lastWell != Lane3_currWell do
		Lane3_Pump = Lane3_currWell+8
		trigger(3)
		Lane3_lastWell = Lane3_currWell
		portout[5]=0
		portout[6]=1
	end
end;

callback portin[6] up   % lane 3B	
	Lane3_currWell = 6
	if Lane3_lastWell != Lane3_currWell do
		Lane3_Pump = Lane3_currWell + 8
		trigger(3)
		Lane3_lastWell = Lane3_currWell
		portout[6]=0
		portout[5]=1
	end
end;

callback portin[7] up   % lane 4A
	Lane4_currWell = 7
	if Lane4_lastWell != Lane4_currWell do
		Lane4_Pump = Lane4_currWell+8
		trigger(4)
		Lane4_lastWell = Lane4_currWell
		portout[7]=0
		portout[8]=1
	end
end;

callback portin[8] up   % lane 4B	
	Lane4_currWell = 8
	if Lane4_lastWell != Lane4_currWell do
		Lane4_Pump = Lane4_currWell + 8
		trigger(4)
		Lane4_lastWell = Lane4_currWell
		portout[8]=0
		portout[7]=1
	end
end;

updates off;

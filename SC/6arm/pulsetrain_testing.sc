% PROGRAM NAME: 	pulsetrain_testing.sc
% AUTHOR: AKG
% DESCRIPTION: 	

% constants    - design your pulsetrain
int pulseLength = 10  	% how long to deliver the reward at home/rip/wait
int pulseInterval = 20  % how long between pulses
int pulseNum = 5        % how many pulses

% variables
int port = 0 % used in the re-priming the pumps function and alloff function only 
int trainCounter = 0
int rewardPump = 9  % set this to pump number you want (9-15)
;

% SMALL reward (home well)
function 10
	trainCounter = 0
  while trainCounter < pulseNum do every pulseInterval % deliver the reward
  	portout[rewardPump]=1 % reward
    do in pulseLength 
    	portout[rewardPump]=0 % reset reward
    end
    trainCounter = trainCounter + 1
  end
end;

%potentially useful additional triggers 

% all off
function 2
	port = 1
	while port < 33 do every 1
		portout[port]=0
		port = port + 1
	end
end;

% reprime pumps
function 3
	port = 9
	while port < 16 do every 5
		portout[port]=flip
		port = port + 1
	end
	do in 100
		port = 9
		while port < 16 do every 5
			portout[port]=flip
			port = port + 1
		end
	end
end;

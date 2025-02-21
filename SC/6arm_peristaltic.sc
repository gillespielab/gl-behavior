% PROGRAM NAME: 	6arm_cued.sc
% AUTHOR: AKG
% DESCRIPTION: pretraining regime 	

% constants
int pulseLength = 10  	% how long to deliver the reward at home/rip/wait
int lockoutPeriod = 5000 	% length of lockout - set by python (default 5 seconds)

% variables
int port = 0 % used when re-priming the pumps
int trainCounter = 0
int rewardPump = 0
int currWell = 0
int lastWell = 0
int homeCount = 0		% number of times rewarded at home
int lockCount = 0		% number of times locked out
int goalCount = 0		% cumulative num outer visits
int goalTotal = 0
int otherCount = 0

% reward lock variables
int _rewardPump = 0
int _rewardLock = 0

;

% display status
function 1
	disp(homeCount)
	disp(lockCount)
	disp(goalCount)
	disp(goalTotal)
	disp(otherCount)
end;

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

% reset the maze
function 4
	trigger(2) % all off
	port = 0
	trainCounter = 0
	rewardPump = 0
	currWell = 0
	lastWell = 0
	homeCount = 0
	lockCount = 0
	goalCount = 0
	goalTotal = 0
	otherCount = 0
	_rewardPump = 0
	_rewardLock = 0
	do in 50
		trigger(3) % reprime pumps
		do in 250
			disp('READY')
		end
	end
end;

% end lockout
function 5
	do in lockoutPeriod
		disp('LOCKEND')
		lastWell = 0
	end
end;

% end epoch
function 6
	disp('STOP')
end;

% ping python every 5 minutes to check if the epoch timed out
function 7
	while port < 100 do every 300000
		disp('PING')
	end
end;

% 50uL reward (home well)
function 10
	if (_rewardLock == 0) do % only give 1 reward at a time
		_rewardLock = 1 % grab the lock
		_rewardPump = rewardPump % get the port for the pump (rewardPump could potentially be changed while the reward is being dispensed)
		trainCounter = 0
		while trainCounter < 3 do every 20 % deliver the reward
			portout[_rewardPump]=1 % reward
			do in pulseLength 
				portout[_rewardPump]=0 % reset reward
			end
			trainCounter = trainCounter + 1
		then do
			disp('50uL reward dispensed')
			disp(_rewardPump) % if there's ever any confusion, this ensures that we can always figure out if a rat actually recieved a reward relatively easilly
			_rewardLock = 0 % release the lock (this allows reward to be given at a different well)
		end
	else do
		disp('REWARD_ERROR')
		disp('reward lock not available, reward not dispensed. CHECK REWARD WELLS IMMEDIATELY')
		disp(rewardPump)
	end
end;

% 100uL reward
function 11
	if (_rewardLock == 0) do
		_rewardLock = 1
		_rewardPump = rewardPump
		trainCounter = 0
		while trainCounter < 7 do every 18 
			portout[_rewardPump]=1 % reward
			do in pulseLength 
				portout[_rewardPump]=0 % reset reward
			end
			trainCounter = trainCounter + 1
		then do
			disp('100uL reward dispensed')
			disp(_rewardPump)
			_rewardLock = 0
		end
	else do
		disp('REWARD_ERROR')
		disp('reward lock not available, reward not dispensed. CHECK REWARD WELLS IMMEDIATELY')
		disp(rewardPump)
	end
end;

% 150uL reward
function 12
	if (_rewardLock == 0) do
		_rewardLock = 1
		_rewardPump = rewardPump
		trainCounter = 0
		while trainCounter < 10 do every 20 
			portout[_rewardPump]=1 % reward
			do in pulseLength 
				portout[_rewardPump]=0 % reset reward
			end
			trainCounter = trainCounter + 1
		then do
			disp('150uL reward dispensed')
			disp(_rewardPump)
			_rewardLock = 0
		end
	else do
		disp('REWARD_ERROR')
		disp('reward lock not available, reward not dispensed. CHECK REWARD WELLS IMMEDIATELY')
		disp(rewardPump)
	end
end;


% CALLBACKS -- EVENT-DRIVEN TRIGGERS

callback portin[1] up
	currWell = 1
	if currWell != lastWell do
		disp('UP 1')
	end
end;

callback portin[1] down
	lastWell = 1
	disp('DOWN 1')
end;


callback portin[2] up
	currWell = 2
	if currWell != lastWell do
		disp('UP 2')
	end
end;

callback portin[2] down
	lastWell = 2
	disp('DOWN 2')
end;

callback portin[3] up
	currWell = 3
	if currWell != lastWell do
		disp('UP 3')
	end
end;

callback portin[3] down
	lastWell = 3
	disp('DOWN 3')
end;

callback portin[4] up
	currWell = 4
	if currWell != lastWell do
		disp('UP 4')
	end
end;

callback portin[4] down
	lastWell = 4
	disp('DOWN 4')
end;

callback portin[5] up
	currWell = 5
	if currWell != lastWell do
		disp('UP 5')
	end
end;

callback portin[5] down
	lastWell = 5
	disp('DOWN 5')
end;

callback portin[6] up
	currWell = 6
	if currWell != lastWell do
		disp('UP 6')
	end
end;

callback portin[6] down
	lastWell = 6
	disp('DOWN 6')
end;

callback portin[7] up
	currWell = 7
	if currWell != lastWell do
		disp('UP 7')
	end
end;

callback portin[7] down
	lastWell = 7
	disp('DOWN 7')
end;


trigger(2) % all off
trigger(7) % ping

;


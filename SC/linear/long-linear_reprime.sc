% a pointer which lets us reuse code when turning pumps on/off
int port

;

% turn all pumps on/off
function 1
    port = 9
    while port < 13 do every 5
        portout[port]=flip
        port = port + 1
    end
end;

% turn the pumps on, wait 100ms, and then turn the pumps off
function 2
    trigger(1)
    do in 150 % controls how much milk is dispensed when re-priming
        trigger(1)
    end
end;

% run the main method
trigger(2)

;

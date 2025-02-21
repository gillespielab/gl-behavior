int port

;

function 1
    port = 9
    while port < 16 do every 10
        portout[port]=flip
        port = port + 1
    end
end;

function 2
    trigger(1)
    do in 100
        trigger(1)
    end
end;

trigger(2)

;

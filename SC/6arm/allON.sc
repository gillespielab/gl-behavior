int port;

function 1
    port = 9
    while port < 17 do every 10
        portout[port]=1
        port = port + 1
    end
end;

trigger(1);


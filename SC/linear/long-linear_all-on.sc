int port;

function 1
    portout[1]=1
    portout[2]=1
    portout[3]=1
    portout[4]=1
    port = 9
    while port < 13 do every 10
        portout[port]=1
        port = port + 1
    end
end;

trigger(1);


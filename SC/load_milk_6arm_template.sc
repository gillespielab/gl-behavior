function 1
    portout[9]=1
    do in 18000
        portout[9]=0
    end
end;

function 2
    portout[10]=1
    do in 13000
        portout[10]=0
    end
end;

function 3
    portout[11]=1
    do in 12000
        portout[11]=0
    end
end;

function 4
    portout[12]=1
    do in 11000
        portout[12]=0
    end
end;

function 5
    portout[13]=1
    do in 13000
        portout[13]=0
    end
end;

function 6
    portout[14]=1
    do in 18000
        portout[14]=0
    end
end;

function 7
    portout[15]=1
    do in 18000
        portout[15]=0
    end
end;

function 8
    trigger(1)
    do in 10
        trigger(2)
    end
    do in 20
        trigger(3)
    end
    do in 30
        trigger(4)
    end
    do in 40
        trigger(5)
    end
    do in 50
        trigger(6)
    end
    do in 60
        trigger(7)
    end
end;

trigger(8)

;

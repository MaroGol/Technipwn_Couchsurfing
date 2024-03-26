var testPin = DebugSymbol.getFunctionByName("test_pin");

Interceptor.attach(testPin, {
    onEnter: function(args) {
        //console.log("test_pin(" + args[0].readCString().trim() + ")");
        console.log("Hijacking test_pin! Returning 1");
    },
    onLeave: function(retval) {
        //console.log(" => ret: " + retval);
        //return retval;
        retval.replace(ptr("0x1")); // <-- replace the return value to 1
    }
});

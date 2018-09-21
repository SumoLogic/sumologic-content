package com.sumologic.hackathontestapp;

import android.accounts.AuthenticatorException;
import android.app.AuthenticationRequiredException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.sql.SQLDataException;
import java.util.concurrent.ThreadLocalRandom;

public class DummyLoggenrator {
    static private Logger log = LoggerFactory.getLogger("zuber-ride-booking");

    static private String[] error = {"java.util.NoSuchElementException: Unable to retrieve customer Info",
            "java.lang.reflect.UndeclaredThrowableException",
            "The specified bucket does not exist",
            "com.amazonaws.services.securitytoken.model.AWSSecurityTokenServiceException: Access denied"};

    static private String[] regions = {"India", "USA", "Poland", "Japan"};

    static private int  getRandInt(int low, int high) {
        return ThreadLocalRandom.current().nextInt(low, high);
    }

    static private void logErrorMessage(String region){
        int index = getRandInt(0, 5);
        String cid = "0000000" + getRandInt(0, 1000) + "A1F" + getRandInt(0, 1000);
        String msg = "Region: " + region + " " + "CustomerId " + cid + "\n";
        try {
            switch (index) {
                case 0:
                    throw new OutOfMemoryError("Error while booking ride");
                case 1:
                    throw new IndexOutOfBoundsException("Error while accessing customer Id");
                case 2:
                    throw new IOException("While accessing device GPS");
                case 3:
                    throw new AuthenticatorException("Fail to authenticate users");
                case 4:
                    throw new SQLDataException("Error while registering request");

            }
        } catch (Throwable e){
            log.error(msg, e);
        }
    }

    static public void generateLog(){
        for (String region: regions) {
            if(getRandInt(0, 5) >= 3 ) {
                logErrorMessage(region);
            }
            if(region.equalsIgnoreCase("india")){
                logErrorMessage(region);
            }
        }
    }
}

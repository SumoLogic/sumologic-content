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

    static private void logNoneErrorLog(String region){
        String[] msgs = {"Sending ride information to Zuber server",
                "Starting position is: Delhi",
                "Ending position is: SumoLogic India",
                "Info received at Zuber server",
                "Pushing info to our ride processing pipeline",
                "Database recovering",
                "To many requests from customer",
                "location service has started"};

        for (String msg: msgs) {
            String cid = "0000000" + getRandInt(0, 1000) + "A1F" + getRandInt(0, 1000);
            String logMessage = "Region: " + region + " " + "CustomerId " + cid + " " + msg;
            int index = getRandInt(0, 3);
            switch (index){
                case 0: log.warn(logMessage); break;
                case 1: log.info(logMessage); break;
                case 2: log.debug(logMessage); break;
            }

        }
    }

    static public void generateLog(){
        for (String region: regions) {
            if(getRandInt(0, 4) >= 3 ) {
                logErrorMessage(region);
            }
            if(region.equalsIgnoreCase("india")){
                logErrorMessage(region);
                logErrorMessage(region);
                logNoneErrorLog(region);
            }
        }
    }
}

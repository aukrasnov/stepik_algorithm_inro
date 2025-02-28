package org.example.data;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class FhvInfo {
    public FhvInfo(String[] arr) {
        dispatching_base_num = arr[0];
        pickup_datetime = LocalDateTime.parse(arr[1], DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
        dropOff_datetime = LocalDateTime.parse(arr[2], DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
        PULocationID = Long.parseLong(arr[3]);
        DOLocationID = Long.parseLong(arr[4]);
        SR_Flag = arr[5];
        Affiliated_base_number = arr[6];
    }
    public FhvInfo(){}
    public String dispatching_base_num;
    public LocalDateTime pickup_datetime;
    public LocalDateTime dropOff_datetime;
    public long PULocationID;
    public long DOLocationID;
    public String SR_Flag;
    public String Affiliated_base_number;


}














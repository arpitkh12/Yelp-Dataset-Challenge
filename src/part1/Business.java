/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package part1;

import com.google.gson.JsonObject;
import java.util.ArrayList;

/**
 *
 * @author tejashree
 */
public class Business {

    String business_id;
    String full_address;
    Hours hours;
    boolean open;
    ArrayList<String> categories;
    String city;
    int review_count;
    String name;
    ArrayList<String> neighborhoods;
    double longitude;
    String state;
    double stars;
    double latitude;
    JsonObject attributes;
    String type;
}

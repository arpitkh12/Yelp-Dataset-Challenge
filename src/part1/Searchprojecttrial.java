/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package part1;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import com.google.gson.Gson;

/**
 *
 * @author tejashree
 */
public class Searchprojecttrial {

	/**
	 * @param args
	 *            the command line arguments
	 */
	public static void main(String[] args) throws FileNotFoundException, IOException {
		// TODO code application logic here
		Gson gson = new Gson();
		File f = new File(
				"/Users/tejashree/Downloads/yelp_dataset_challenge_academic_dataset_business/yelp_academic_dataset_business.json.ab");
		BufferedReader reader = new BufferedReader(new FileReader(f));
		String line = null;
		line = reader.readLine();
		try {
			while ((line = reader.readLine()) != null) {

				Business r = gson.fromJson(line, Business.class);
				System.out.println(r.business_id);
				System.out.println(r.full_address);
				if (r.hours.monday != null)
					System.out.println("hours " + r.hours.monday.open);
				System.out.println(r.open);
				System.out.println(r.categories);
				for (String s : r.categories)
					System.out.println(s);
				System.out.println(r.attributes.toString());

			}

		} catch (Exception e) {
			System.out.println(line);
			e.printStackTrace();
		} finally {
			reader.close();
		}

	}

}

package mongo.java;

import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import com.mongodb.MongoClient;

public class MongoTest {
	public static void main(String[] args) {

		try {

			// To connect to mongodb server
			MongoClient mongoClient = new MongoClient("localhost", 27017);

			// Now connect to your databases
			DB db = mongoClient.getDB("yelp_data");
			System.out.println("Connect to database successfully");
			DBCollection coll = db.getCollection("business_data");
			System.out.println("Collection created successfully");
			DBCursor cursor = coll.find();
			coll.createIndex("business_id");
//			coll.index
			System.out.println("Index Created Successfully");
			// int i = 1;

			// while (cursor.hasNext()) {
			// System.out.println("Inserted Document: " + i);
			// System.out.println(cursor.next());
			// i++;
			// }
		} catch (Exception e) {
			System.err.println(e.getClass().getName() + ": " + e.getMessage());
		}
	}
}

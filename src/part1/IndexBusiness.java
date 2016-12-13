package part1;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.Set;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.SortedSetDocValuesField;
import org.apache.lucene.document.StoredField;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.IndexWriterConfig.OpenMode;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.BytesRef;

import com.google.gson.Gson;
import com.google.gson.JsonObject;

/**
 *
 * @author tejashree
 */
public class IndexBusiness {

	/**
	 * @param args
	 *            the command line arguments
	 */
	public static void main(String[] args) throws FileNotFoundException, IOException {
		// TODO code application logic here
		Analyzer analyzer = new StandardAnalyzer();
		Directory dir = FSDirectory.open(Paths.get("index_business"));
		IndexWriterConfig iwc = new IndexWriterConfig(analyzer);
		iwc.setOpenMode(OpenMode.CREATE);
		IndexWriter writer = new IndexWriter(dir, iwc);

		Gson gson = new Gson();
		File f = new File("/Users/arpitkhandelwal/Downloads/yelp_dataset_challenge_academic_dataset/business.json");
		BufferedReader reader = new BufferedReader(new FileReader(f));
		String line = null;
		int count = 0;
		try {
			while ((line = reader.readLine()) != null) {
				JsonObject r = gson.fromJson(line, JsonObject.class);
				// System.out.println(r.get("attributes").toString());
				JsonObject a = gson.fromJson(r.get("attributes").toString(), JsonObject.class);
				// a.keySet();
				Set alist = a.entrySet();

				Business r1 = gson.fromJson(line, Business.class);
				Document luceneDoc = new Document();
				luceneDoc.add(new TextField("fulladdress", r1.full_address, Field.Store.YES));
				luceneDoc.add(new StringField("businessid", r1.business_id, Field.Store.YES));
				luceneDoc.add(new StringField("city", r1.city, Field.Store.YES));
				luceneDoc.add(new StringField("open", String.valueOf(r1.open), Field.Store.YES));
				luceneDoc.add(new StringField("name", r1.name, Field.Store.YES));
				luceneDoc.add(new StoredField("longitude", r1.longitude));
				luceneDoc.add(new StoredField("latitude", r1.latitude));
				luceneDoc.add(new StoredField("reviewcount", r1.review_count));
				luceneDoc.add(new StringField("state", r1.state, Field.Store.YES));
				luceneDoc.add(new StoredField("stars", r1.stars));
				luceneDoc.add(new StringField("type", r1.type, Field.Store.YES));
				for (String c : r1.categories)
					luceneDoc.add(new SortedSetDocValuesField("category", new BytesRef(c)));
				for (String c : r1.neighborhoods)
					luceneDoc.add(new SortedSetDocValuesField("neighborhoods", new BytesRef(c)));
				for (Object attribute : alist) {
					String attributedetail[] = attribute.toString().split("=");
					String key = attributedetail[0].trim();
					String value = attributedetail[1].trim();
					luceneDoc.add(new TextField(key, value, Field.Store.YES));
				}
				writer.addDocument(luceneDoc);
			}

		} catch (Exception e) {
			System.out.println(line);
			e.printStackTrace();
		} finally {
			reader.close();
			writer.close();
		}

	}

}

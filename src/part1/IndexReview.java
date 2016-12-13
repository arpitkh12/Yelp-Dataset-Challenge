package part1;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Paths;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.IndexWriterConfig.OpenMode;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

import com.google.gson.Gson;

/**
 *
 * @author tejashree
 */
public class IndexReview {

	/**
	 * @param args
	 *            the command line arguments
	 */
	public static void main(String[] args) throws IOException {
		// TODO code application logic here
		String indexDir = "/Users/arpitkhandelwal/Downloads/yelp_dataset_challenge_academic_dataset/review.json";
		Analyzer analyzer = new StandardAnalyzer();
		Directory dir = FSDirectory.open(Paths.get("index"));
		IndexWriterConfig iwc = new IndexWriterConfig(analyzer);
		iwc.setOpenMode(OpenMode.CREATE);
		IndexWriter writer = new IndexWriter(dir, iwc);

		Gson gson = new Gson();
		File f = new File("/Users/arpitkhandelwal/Downloads/yelp_dataset_challenge_academic_dataset/review.json");
		BufferedReader reader = new BufferedReader(new FileReader(f));
		String line = null;
		line = reader.readLine();
		try {
			while ((line = reader.readLine()) != null) {
				// System.out.println(line);
				Review r = gson.fromJson(line, Review.class);
				Document luceneDoc = new Document();
				luceneDoc.add(new TextField("text", r.text, Field.Store.YES));
				luceneDoc.add(new StringField("business_id", r.business_id, Field.Store.YES));
				luceneDoc.add(new StringField("user_id", r.user_id, Field.Store.YES));
				luceneDoc.add(new StringField("stars", String.valueOf(r.stars), Field.Store.YES));
				luceneDoc.add(new StringField("type", r.type, Field.Store.YES));
				luceneDoc.add(new StringField("date", r.date, Field.Store.YES));
				luceneDoc.add(new StringField("votes_funny", String.valueOf(r.votes.funny), Field.Store.YES));
				luceneDoc.add(new StringField("votes_useful", String.valueOf(r.votes.useful), Field.Store.YES));
				luceneDoc.add(new StringField("votes_cool", String.valueOf(r.votes.cool), Field.Store.YES));
				writer.addDocument(luceneDoc);
			}
		} finally {
			reader.close();
			writer.close();
		}
	}
}

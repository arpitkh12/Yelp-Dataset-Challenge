package part1;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Paths;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.IndexWriterConfig.OpenMode;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

import com.csvreader.CsvReader;

public class IndexData {
	private static final String DATA_PATH = "data1.csv";
	private static final String LUCENE_INDEX_PATH = "index/index_business";

	public static void csvReader() throws IOException {
		CsvReader csv = new CsvReader(DATA_PATH);
		int count = 0;
		while (csv.readRecord()) {
			String s = csv.getRawRecord();
			System.out.println(count + "\t" + s);
			count++;
		}
	}

	@SuppressWarnings({ "resource", "unused" })
	public static void generateIndex() {
		try {
			CsvReader csv = new CsvReader(DATA_PATH);
			Analyzer analyzer = new StandardAnalyzer();
			Directory dir = FSDirectory.open(Paths.get(LUCENE_INDEX_PATH));
			IndexWriterConfig iwc = new IndexWriterConfig(analyzer);
			iwc.setOpenMode(OpenMode.CREATE);
			IndexWriter writer = new IndexWriter(dir, iwc);

			String line = "";
			String previous = "";
			String splitValue = ",\"\\[";
			while (csv.readRecord()) {
				line = csv.getRawRecord();
//				System.out.println(line);
				String[] str = line.split(splitValue);
				Document luceneDoc = new Document();
				// if (str.length < 2) {
				// previous = line;
				// }
				if (str.length == 2) {
					luceneDoc.add(new TextField("text", str[0], Field.Store.YES));
					luceneDoc.add(new TextField("category", str[1].replaceAll("]", ""), Field.Store.YES));
					writer.addDocument(luceneDoc);
					previous = "";
				}

			}

			writer.close();
			// br.close();

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public static void main(String[] args) {
//		try {
			generateIndex();
//		} 
//		catch (FileNotFoundException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}
//		// generateIndex();
//		catch (IOException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}
	}

}

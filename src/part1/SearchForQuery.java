package part1;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.queryparser.xml.ParserException;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.search.similarities.BM25Similarity;
import org.apache.lucene.search.similarities.Similarity;
import org.apache.lucene.store.FSDirectory;

import com.csvreader.CsvReader;

public class SearchForQuery {

	public static final String INDEX_PATH1 = "index/index_business";
	public static final String INDEX_PATH2 = "index_tip";

	@SuppressWarnings({ "rawtypes", "unchecked", "resource" })
	public static void main(String[] args)
			throws IOException, ParserException, org.apache.lucene.queryparser.classic.ParseException {
		CsvReader csv = new CsvReader("reviews_new2.csv");
		String line;
		String splitValue = ",\"\\[";
		double sum = 0;
		int countRecords = 0;
		while (csv.readRecord()) {
			line = csv.getRawRecord();
			countRecords++;
			String[] str = line.split(splitValue);
			String[] category = (str[1].replaceAll("]", "")).split(",");
			List<String> ans = new ArrayList<>();
			for (String s : category)
				ans.add(s);
			HashMap<String, Integer> map = new HashMap<String, Integer>();
			String queryString = str[0];
			Similarity similarity = new BM25Similarity();
			IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(INDEX_PATH1)));
			IndexSearcher searcher = new IndexSearcher(reader);
			Analyzer analyzer = new StandardAnalyzer();
			searcher.setSimilarity(similarity);
			QueryParser parser = new QueryParser("text", analyzer);
			Query q = parser.parse(queryString);
			TopDocs results = searcher.search(q, 1000);
			ScoreDoc[] docs = results.scoreDocs;
			for (int i = 0; i < docs.length; i++) {
				Document doc = searcher.doc(docs[i].doc);
				String result = doc.get("category").trim().replaceAll("[^A-Za-z,\\s]", "");
				String[] re = result.split(",");
				for (String r : re) {
					if (r.isEmpty()) {
						System.out.println("adsadsad" + doc.get("category"));
					}
					if (map.containsKey(r)) {
						int x = map.get(r);
						map.put(r, x + 1);
					} else {
						map.put(r, 1);
					}
				}
			}

			System.out.println(map);

			Map<String, Integer> map1 = new HashMap<String, Integer>();
			List<String> list = new ArrayList<String>();
			map.entrySet().stream().sorted(Map.Entry.<String, Integer>comparingByValue().reversed()).limit(10)
					.forEach(e -> {
						if (e.getValue() > 10)
							list.add(e.getKey().toLowerCase().trim());
						map1.put(e.getKey(), e.getValue());
						System.out.println(e.getValue() + "\t" + e.getKey());
					});
			System.out.println(list);
			int counter = 0;
			for (String s : list) {
				if (ans.contains(s.trim().replaceAll(" ", ""))) {
					counter++;
				}
			}
			System.out.println(list);
			System.out.println(ans);
			HashSet<String> set = new HashSet<>();
			set.addAll(list);
			set.addAll(ans);
			double jaccardSimilarity = (double) counter / (double) set.size();
			if(list.size()>0){
				System.out.println(map);
			}
			sum += jaccardSimilarity;
		}
		System.out.println("*****");
		System.out.println("Actual Jaccard Similarity");
		System.out.println("Sum" + sum);
		System.out.println("Records count" + countRecords);
		System.out.println(sum / countRecords);
	}

}

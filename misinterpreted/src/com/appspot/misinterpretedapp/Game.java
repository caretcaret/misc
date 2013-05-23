package com.appspot.misinterpretedapp;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.content.Context;

// Game stores the DATA, does not handle the game input/output. GameActivity and DrawView do that.
public class Game {
	public int numTextSlides;
	public int numDrawSlides;
	public int currentSlideIdx = -1; // goes from 0 to (numPlayers - 1). -1 if game is not yet started.
	
	// Which game are we doing?
	final static int MODE_OFFLINE = 0;
	final static int MODE_PRIVATE = 1;
	final static int MODE_PUBLIC = 2;
	int mode;
	
	// What type of slide is this?
	final static int SLIDE_TEXT = 3;
	final static int SLIDE_DRAW = 4;
	final static int SLIDE_END = 5;
	
	// arrays for storing slide data.
	// slide 1 = textSlide[0], slide 2 = drawSlide[0], slide 3 drawSlide[1], etc.
	// Overloaded store() will automatically choose the right place to store to.
	private String[] descriptions;
	private Drawing[] drawings;
	
	// Working variables to pass to store().
	protected String bufferDescription = "";
	protected Drawing bufferDrawing = new Drawing();
	
	// Display metrics of the drawing screen for x-compatibility
	private float width;
	private float height;
	private float dp;
	
	//private long beginTime; // Use date objects?
	//private long endTime;
	
	// instantiate a new game object for data storage
	public Game(int numPlayers, int mode, float width, float height, float dp) {
		// Split numPlayers into number of text and draw slides. If numPlayers is odd, numTextSlides should
		// be one more than numDrawSlides.
		numTextSlides = (numPlayers+1)/2; //(numPlayers + 1)/2 uses integer division
		numDrawSlides = numPlayers/2;
		descriptions = new String[numTextSlides];
		drawings = new Drawing[numDrawSlides];
		this.mode = mode;
		this.width = width;
		this.height = height;
		this.dp = dp;
	}
	
	// Starts the next slide and returns the slideID of that slide. If the end of the game is reached,
	// nothing happens. Otherwise, data is saved from Game.bufferDescription or Game.bufferDrawing first,
	// buffer is reset, before the Game data structure is ready for the next slide.
	public int startNextSlide() {
		switch(getSlideType()) {
		case SLIDE_END: return currentSlideIdx;
		case SLIDE_TEXT:
			if (currentSlideIdx >= 0)
				store(bufferDescription);
			bufferDescription = "";
			return ++currentSlideIdx; // increment currentSlideIdx, then return it.
		case SLIDE_DRAW:
			if (currentSlideIdx >= 0)
				store(bufferDrawing);
			bufferDrawing = new Drawing();
			return ++currentSlideIdx;
		default: return -1; // shouldn't happen
		}
	}
	
	// Usage: use after bufferDescription is set to the user's input
	public void store(String s) {
		descriptions[currentSlideIdx/2] = s;
	}
	
	public void store(Drawing d) {
		drawings[currentSlideIdx/2] = d;
	}
	
	public int getSlideType() {
		if (currentSlideIdx >= numTextSlides + numDrawSlides)
			return SLIDE_END;
		if (currentSlideIdx % 2 == 0)
			return SLIDE_TEXT;
		else
			return SLIDE_DRAW;
	}
	
	public int getSlideIdx() {
		return currentSlideIdx;
	}
	
	public String getPreviousDescription() {
		int prevSlideIdx = currentSlideIdx - 1;
		if (prevSlideIdx >= 0)
			return descriptions[prevSlideIdx/2];
		else
			return "";
	}
	
	public Drawing getPreviousDrawing() {
		int prevSlideIdx = currentSlideIdx - 1;
		if (prevSlideIdx >= 0)
			return drawings[prevSlideIdx/2];
		else
			return new Drawing();
	}
	
	public void loadDescriptions(String[] descriptions) {
		this.descriptions = descriptions;
	}
	
	public void loadDrawings(Drawing[] drawings) {
		this.drawings = drawings;
	}

	// Mirrors unjsonify().
	public String jsonify() throws JSONException {
		JSONObject jGameObj = new JSONObject();
		jGameObj.put("width", new Double(width));
		jGameObj.put("height", new Double(height));
		jGameObj.put("dp", new Double(dp));
		jGameObj.put("mode", new Integer(mode));
		JSONArray jDescriptions = new JSONArray();
		JSONArray jDrawings = new JSONArray();
		
		// store descriptions into JSONArray jDescriptions
		for (int i = 0; i < numTextSlides; i++) {
			jDescriptions.put(i, descriptions[i]);
		}
		
		// store drawings in JSONArray jDrawings
		for (int i = 0; i < numDrawSlides; i++) { // handle each drawing slide, drawings[i]
			ArrayList<PenAction> paArr = drawings[i].getActionList();
			JSONObject jDrawSlide = new JSONObject();
			JSONArray jPA = new JSONArray();
			for (int j = 0; j < paArr.size(); j++) {
				JSONObject jPenAction = new JSONObject();
				PenAction pa = paArr.get(j);
				jPenAction.put("action", new Integer(pa.action));
				jPenAction.put("x", new Double(pa.x));
				jPenAction.put("y", new Double(pa.y));
				jPenAction.put("size", new Double(pa.size));
				jPenAction.put("color", new Integer(pa.color));
				jPA.put(j, jPenAction);
			}
			jDrawSlide.put("actions", jPA);
			jDrawings.put(i, jDrawSlide);
		}
		
		jGameObj.put("descriptions", jDescriptions);
		jGameObj.put("drawings", jDrawings);
		return jGameObj.toString();
	}
	
	public static Game unjsonify(String jString) throws JSONException {
		// get simple data types from the JSON string
		JSONObject jGameObj = new JSONObject(jString);
		float width = (float) jGameObj.getDouble("width");
		float height = (float) jGameObj.getDouble("height");
		float dp = (float) jGameObj.getDouble("dp");
		int mode = jGameObj.getInt("mode");
		JSONArray jDescriptions = jGameObj.getJSONArray("descriptions");
		JSONArray jDrawings = jGameObj.getJSONArray("drawings");
		int numTextSlides = jDescriptions.length();
		int numDrawSlides = jDrawings.length();
		String[] descriptions = new String[numTextSlides];
		Drawing[] drawings = new Drawing[numDrawSlides];
		
		// get the description array of strings.
		for (int i = 0; i < numTextSlides; i++) {
			descriptions[i] = jDescriptions.getString(i);
		}
		
		// get the drawings array. Each array element holds a Drawing object
		for (int i = 0; i < numDrawSlides; i++) { // handle each drawing slide in the drawing array
			JSONObject jDrawSlide = jDrawings.getJSONObject(i);
			JSONArray jActions = jDrawSlide.getJSONArray("actions");
			Drawing drawSlide = new Drawing();
			for (int j = 0; j < jActions.length(); j++) { // handle each PenAction in the slide
				JSONObject jPenAction = jActions.getJSONObject(j);
				PenAction pa = new PenAction();
				pa.action = jPenAction.getInt("action");
				pa.x = (float) jPenAction.getDouble("x");
				pa.y = (float) jPenAction.getDouble("y");
				pa.size = (float) jPenAction.getDouble("size");
				pa.color = jPenAction.getInt("color");
				drawSlide.addRawPenAction(pa);
			}
			drawings[i] = drawSlide;
		}
		
		Game game = new Game(numTextSlides+numDrawSlides, mode, width, height, dp);
		game.loadDescriptions(descriptions);
		game.loadDrawings(drawings);
		return game;
	}
	
	public String save(Context context, String filename, int mode) {
		if (filename == null) {
			// if no name is given to save(), then generate a name based on the timestamp
			if (mode == MODE_OFFLINE) filename = "Offline Game " + System.currentTimeMillis();
			// TODO base filenames on id of game given by server
			else if (mode == MODE_PRIVATE) filename = "Online Private Game " + System.currentTimeMillis();
			else if (mode == MODE_PUBLIC) filename = "Online Public Game " + System.currentTimeMillis();
		}
		try {
			FileOutputStream fos = context.openFileOutput(filename, Context.MODE_PRIVATE);
			fos.write(this.jsonify().getBytes());
			fos.close();
			return filename;
		} catch (FileNotFoundException e) {
			return null;
		} catch (IOException e) {
			return null;
		} catch (JSONException e) {
			return null;
		}
	}
	
	public static String[] getGameList(Context context) {
		return context.fileList();
	}
	
	public static Game open(Context context, String filename)
			throws FileNotFoundException, JSONException, IOException {
		BufferedReader r = new BufferedReader(new InputStreamReader(context.openFileInput(filename)));
		StringBuilder jsonData = new StringBuilder(); // use StringBuilder to optimize
		String line;
		while ((line = r.readLine()) != null) {
		    jsonData.append(line);
		}
		Game game = Game.unjsonify(jsonData.toString());
		return game;
	}
	
	public String getTextSlide(int i) { // where i is the slide number of the overall game.
		return descriptions[i/2];
	}
	public Drawing getDrawSlide(int i) {
		return drawings[i/2];
	}
	
	public void clean() {
		for (int i = 0; i < numTextSlides; i++) {
			if (descriptions[i] == null) {
				String[] newDescriptions = new String[i];
				System.arraycopy(descriptions, 0, newDescriptions, 0, i);
				descriptions = newDescriptions;
				numTextSlides = descriptions.length;
				break;
			}
		}
		for (int i = 0; i < numDrawSlides; i++) {
			if (drawings[i] == null) {
				Drawing[] newDrawings = new Drawing[i];
				System.arraycopy(drawings, 0, newDrawings, 0, i);
				drawings = newDrawings;
				numDrawSlides = drawings.length;
				break;
			}
		}
	}
}
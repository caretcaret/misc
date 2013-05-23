package com.appspot.misinterpretedapp;

import android.app.ListActivity;
import android.content.Intent;
import android.content.res.Configuration;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

public class GameListActivity extends ListActivity {
	
	String[] listToShow = {"You have no saved games."};
	int numGames = 0;
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		
		// Remove the title bar and set full screen mode.
		getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
				WindowManager.LayoutParams.FLAG_FULLSCREEN);
		requestWindowFeature(Window.FEATURE_NO_TITLE);
		
        String[] listGames = Game.getGameList(GameListActivity.this);
        // If there are more than 0 files, assign the list of filenames.
        // If it is 0, then leave the default text (which will not do anything onClick)
        numGames = listGames.length;
        if (numGames > 0)
        	listToShow = listGames;
        
		setListAdapter(new ArrayAdapter<String>(this, R.layout.gamelist, listToShow));
		ListView lv = getListView();
		lv.setTextFilterEnabled(true);
		// TODO set background
		// a bit buggy //lv.setBackgroundResource(R.drawable.linedpaper_repeat);
		
		lv.setOnItemClickListener(new OnItemClickListener() {
		    public void onItemClick(AdapterView<?> parent, View view,
		        int position, long id) { 
		    	if (numGames > 0) {
		    		Intent intent = new Intent(GameListActivity.this, ViewActivity.class);
		    		String filename = ((TextView) view).getText().toString();
		    		intent.putExtra("filename", filename);
		    		GameListActivity.this.startActivity(intent);
		    	} else {
		    		// do nothing onclick if there are no games to show.
		    	}
		    }
		  });
	}

	// Prevent orientation change from landscape.
	public void onConfigurationChanged(Configuration newConfig) {
		// ignore orientation/keyboard change
		super.onConfigurationChanged(newConfig);
	}
}
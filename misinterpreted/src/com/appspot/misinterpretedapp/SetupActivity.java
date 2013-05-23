package com.appspot.misinterpretedapp;


import android.app.TabActivity;
import android.content.Context;
import android.content.Intent;
import android.content.res.Configuration;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.TabHost;
import android.widget.TextView;
import android.widget.Toast;

public class SetupActivity extends TabActivity {
	
	
	// Limits on the number of players allowed.
	final int lowerLimitPlayers = 5;
	final int upperLimitPlayers = 9001;
	
	boolean warnedTooFewPlayers = false;
	boolean warnedTooManyPlayers = false;
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		
		// Remove the title bar and set full screen mode.
		getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
				WindowManager.LayoutParams.FLAG_FULLSCREEN);
		requestWindowFeature(Window.FEATURE_NO_TITLE);
		
		// Activate the view
		setContentView(R.layout.setup);
		
		// Setup tabs
		TabHost mTabHost = getTabHost();
        mTabHost.addTab(mTabHost.newTabSpec("offline").setIndicator("Pass-n-Play", getResources().getDrawable(R.drawable.icon)).setContent(R.id.layoutOffline));
        mTabHost.addTab(mTabHost.newTabSpec("private").setIndicator("Online Private", getResources().getDrawable(R.drawable.icon)).setContent(R.id.layoutPrivate));
        mTabHost.addTab(mTabHost.newTabSpec("public").setIndicator("Online Public", getResources().getDrawable(R.drawable.icon)).setContent(R.id.layoutPublic));
        mTabHost.setCurrentTab(0);
        
        // Add functionality to player number buttons
        Button buttonSubtractPlayers = (Button) findViewById(R.id.buttonSubtractPlayers);
        Button buttonAddPlayers = (Button) findViewById(R.id.buttonAddPlayers);
        
        buttonSubtractPlayers.setOnClickListener(new View.OnClickListener() {

        	@Override
        	public void onClick(View v) {
        		TextView textNumPlayers = (TextView) findViewById(R.id.textNumPlayers);
        		try {
        			int numPlayers = Integer.parseInt(textNumPlayers.getText().toString());
        			// do not decrement number of players if it is greater than 5
        			if (numPlayers > lowerLimitPlayers) {
        				numPlayers--;
        			} else {
        				if (!warnedTooFewPlayers) {
        					Toast.makeText(SetupActivity.this, "This game will not work for fewer than " + lowerLimitPlayers + " players.", Toast.LENGTH_SHORT).show();
        					warnedTooFewPlayers = true;
        				}
        			}
        			textNumPlayers.setText(Integer.toString(numPlayers));
        		} catch (Exception e) {
        			textNumPlayers.setText(e.toString());
        		}
        	}
        });
        
        buttonAddPlayers.setOnClickListener(new View.OnClickListener() {
        	@Override
        	public void onClick(View v) {
        		TextView textNumPlayers = (TextView) findViewById(R.id.textNumPlayers);
        		try {
        			int numPlayers = Integer.parseInt(textNumPlayers.getText().toString());
        			if (numPlayers < upperLimitPlayers) {
        				numPlayers++;
        			} else {
        				if (!warnedTooManyPlayers) {
        					Toast.makeText(SetupActivity.this, "IT'S OVER " + (upperLimitPlayers - 1) + "!", Toast.LENGTH_SHORT).show();
        					warnedTooManyPlayers = true;
        				}
        			}
        			textNumPlayers.setText(Integer.toString(numPlayers));
        		} catch (Exception e) {
        			textNumPlayers.setText(e.toString());
        		}
        	}
        });
        
        // Open the GameActivity when the begin button is clicked. Transfer data about the game to be played.
        Button buttonOfflineBegin = (Button) findViewById(R.id.buttonOfflineBegin);
        buttonOfflineBegin.setOnClickListener(new View.OnClickListener() {
        	@Override
        	public void onClick(View v) {
        		Context context = v.getContext();
				Intent intent = new Intent(context, GameActivity.class);
				
				TextView textNumPlayers = (TextView) findViewById(R.id.textNumPlayers);
				
				try {
				intent.putExtra("numPlayers", Integer.parseInt(textNumPlayers.getText().toString()));
				intent.putExtra("mode", Game.MODE_OFFLINE);
				context.startActivity(intent);
				finish();
				} catch (Exception e) {
					textNumPlayers.setText(e.toString());
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
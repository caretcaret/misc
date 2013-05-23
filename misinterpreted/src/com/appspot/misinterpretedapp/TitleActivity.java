package com.appspot.misinterpretedapp;



import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.res.Configuration;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;

public class TitleActivity extends Activity {
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		
		// Remove the title bar and set full screen mode.
		getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
				WindowManager.LayoutParams.FLAG_FULLSCREEN);
		requestWindowFeature(Window.FEATURE_NO_TITLE);
		
		// Activate the view
		setContentView(R.layout.title);
		
		Button buttonLogin = (Button) findViewById(R.id.buttonLogin);
		buttonLogin.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				Context context = v.getContext();
				Intent intent = new Intent(context, LoginActivity.class);
				context.startActivity(intent);
			}
		});
		
		Button buttonPlay = (Button) findViewById(R.id.buttonPlay);
		buttonPlay.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				Context context = v.getContext();
				Intent intent = new Intent(context, SetupActivity.class);
				context.startActivity(intent);
			}
		});
		
		Button buttonView = (Button) findViewById(R.id.buttonView);
		buttonView.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				Context context = v.getContext();
				Intent intent = new Intent(context, GameListActivity.class);
				context.startActivity(intent);
			}
		});
		
		Button buttonInstructions = (Button) findViewById(R.id.buttonInstructions);
		buttonInstructions.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				Context context = v.getContext();
				Intent intent = new Intent(context, InstructionsActivity.class);
				context.startActivity(intent);
			}
		});
	}

	// Prevent orientation change from landscape.
	public void onConfigurationChanged(Configuration newConfig) {
		// ignore orientation/keyboard change
		super.onConfigurationChanged(newConfig);
	}
}
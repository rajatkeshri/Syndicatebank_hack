package com.example.blockchain;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class Main2Activity extends AppCompatActivity {

    Button newUser;
    TextView userName;

    String pre = "Hi ";
    String post = "Your account is registered.";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);

        newUser = (Button) findViewById(R.id.button4);
        userName = (TextView) findViewById(R.id.textView7);

        String name = getIntent().getStringExtra("NAME");
        userName.setText(pre + name + ". " + post);

        newUser.setOnClickListener(user);
    }

    private View.OnClickListener user = new View.OnClickListener() {
        @Override
        public void onClick(View view) {
            Intent intent = new Intent(Main2Activity.this, MainActivity.class);
            startActivity(intent);
        }
    };
}

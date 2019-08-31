package com.example.blockchain;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.app.DatePickerDialog;
import android.app.DatePickerDialog.OnDateSetListener;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.provider.OpenableColumns;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.util.Calendar;

public class MainActivity extends AppCompatActivity {

    EditText name, date;
    TextView dateView, fileName;
    Button upload, submit;
    Spinner dropDown;
    ProgressDialog progress;
    Calendar calendar;
    int year, month, day;
    String[] gender = new String[]{"MALE", "FEMALE"};

    private static final int FILE_SELECT_CODE = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        name = (EditText) findViewById(R.id.editText);
        date = (EditText) findViewById(R.id.editText4);
        fileName = (TextView) findViewById(R.id.textView6);
        upload = (Button) findViewById(R.id.button);
        submit = (Button) findViewById(R.id.button2);
        dropDown = (Spinner) findViewById(R.id.spinner);
        calendar = Calendar.getInstance();

        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, gender);
        dropDown.setAdapter(adapter);

        date.setOnClickListener(setDate);
        upload.setOnClickListener(showFileChooser);
        submit.setOnClickListener(successful);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        if (requestCode == FILE_SELECT_CODE) {
            if (resultCode == RESULT_OK) {
                // Get the Uri of the selected file
                Uri uri = data.getData();
                Log.d("TAG", "File URI: " + uri);
                // Get the path
                String path = getPath(this, uri);
                Log.d("TAG", "File Path: " + path);
                fileName.setText(path);
                // Get the file instance
                // File file = new File(path);
                // Initiate the upload
            }
        }
        super.onActivityResult(requestCode, resultCode, data);
    }

    private View.OnClickListener successful = new View.OnClickListener() {
        @Override
        public void onClick(View view) {

            progress = new ProgressDialog(MainActivity.this);
            progress.setTitle("Please Wait!");
            progress.setMessage("Uploading & Verifying");
            progress.setCancelable(false);
            progress.setProgressStyle(ProgressDialog.STYLE_SPINNER);
            progress.show();

            Handler handler = new Handler();
            handler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    progress.dismiss();

                    Intent intent = new Intent(MainActivity.this, Main2Activity.class);
                    intent.putExtra("NAME", name.getText().toString());
                    startActivity(intent);
                }
            }, 5000);
        }
    };

    private View.OnClickListener showFileChooser = new View.OnClickListener() {
        @Override
        public void onClick(View view) {
            Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
            intent.setType("*/*");
            intent.addCategory(Intent.CATEGORY_OPENABLE);

            try {
                startActivityForResult(
                        Intent.createChooser(intent, "Select a File to Upload"),
                        FILE_SELECT_CODE);
            } catch (android.content.ActivityNotFoundException ex) {
                // Potentially direct the user to the Market with a Dialog
                Toast.makeText(getApplicationContext(), "Please install a File Manager.",
                        Toast.LENGTH_SHORT)
                        .show();
            }
        }
    };

    private View.OnClickListener setDate = new View.OnClickListener() {
        @Override
        public void onClick(View view) {

            final Calendar c = Calendar.getInstance();
            year = c.get(Calendar.YEAR);
            month = c.get(Calendar.MONTH);
            day = c.get(Calendar.DAY_OF_MONTH);


            DatePickerDialog datePickerDialog = new DatePickerDialog(getApplicationContext(),
                    new OnDateSetListener() {
                        @Override
                        public void onDateSet(DatePicker view, int year,
                                              int monthOfYear, int dayOfMonth) {

                            date.setText(dayOfMonth + "-" + (monthOfYear + 1) + "-" + year);

                        }
                    }, year, month, day);
            datePickerDialog.show();
        }
    };

    public String getPath(Context context, Uri uri) {
        String result = null;
        if (uri.getScheme().equals("content")) {
            Cursor cursor = getContentResolver().query(uri, null, null, null, null);
            try {
                if (cursor != null && cursor.moveToFirst()) {
                    result = cursor.getString(cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME));
                }
            } finally {
                cursor.close();
            }
        }

        if (result == null) {
            result = uri.getPath();
            int cut = result.lastIndexOf('/');
            if (cut != -1) {
                result = result.substring(cut + 1);
            }
        }
        return result;
    }
}

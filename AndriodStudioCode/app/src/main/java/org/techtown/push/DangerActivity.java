package org.techtown.push;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.graphics.drawable.GradientDrawable;
import android.os.AsyncTask;
import android.os.Bundle;
import android.text.method.ScrollingMovementMethod;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Calendar;

public class DangerActivity extends AppCompatActivity {

    TextView textView; //결과를 띄어줄 TextView
    TextView scrollView;
    TextView scrollView2;
    TextView scrollView3;
    Document doc = null;
    TextView textView2;
    TextView textView3;
    TextView textView4;
    TextView textView5;
    TextView textView6;
    String[] log_list = { };
    String[] time_list = { };
    String today = "";
    String yesterday = "";
    String byesterday = "";
    String today_t = "";
    String yesterday_t = "";
    String byesterday_t = "";



    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_danger);

        scrollView=findViewById(R.id.DangerView);
        scrollView2=findViewById(R.id.DangerView2);
        scrollView3=findViewById(R.id.DangerView3);
        scrollView.setMovementMethod(new ScrollingMovementMethod());
        scrollView2.setMovementMethod(new ScrollingMovementMethod());
        scrollView3.setMovementMethod(new ScrollingMovementMethod());


        textView = (TextView) findViewById(R.id.DangerView);
        textView2 = (TextView) findViewById(R.id.DangerView2);
        textView3 = (TextView) findViewById(R.id.DangerView3);
        textView4 = (TextView) findViewById(R.id.danger_header1);
        textView5 = (TextView) findViewById(R.id.danger_header2);
        textView6 = (TextView) findViewById(R.id.danger_header3);

        new AsyncTask() {
            @Override
            protected Object doInBackground(Object[] params) {
                SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
                Calendar calendar = Calendar.getInstance(); // 오늘날짜
                String date = sdf.format(calendar.getTime());
                String today_m = date.substring(5,7);
                String today_d = date.substring(8);
                calendar.add(Calendar.DATE, -1);
                String date1 = sdf.format(calendar.getTime());
                String yesterday_m = date1.substring(5,7);
                String yesterday_d = date1.substring(8);
                calendar.add(Calendar.DATE, -1);
                String date2 = sdf.format(calendar.getTime());
                String b_yesterday_m = date2.substring(5,7);
                String b_yesterday_d = date2.substring(8);

                try {
                    doc = Jsoup.connect("http://192.168.30.3:5000/log").get();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                time_list = doc.select("span.time").text().split(" ");
                log_list = doc.select("span.log").text().split(" ");
                for(int i = 0; i < time_list.length; i++){
                    if(time_list[i].substring(5,7).equals(today_m) && time_list[i].substring(8,10).equals(today_d)){
                        today = time_list[i].substring(0,13);
                        today_t += time_list[i].substring(13) + " - " + log_list[0] + "\n";
                    }
                    if(time_list[i].substring(5,7).equals(yesterday_m) && time_list[i].substring(8,10).equals(yesterday_d)){
                        yesterday = time_list[i].substring(0,13);
                        yesterday_t += time_list[i].substring(13) + " - " + log_list[0] + "\n";
                    }
                    if(time_list[i].substring(5,7).equals(b_yesterday_m) && time_list[i].substring(8,10).equals(b_yesterday_d)){
                        byesterday = time_list[i].substring(0,13);
                        byesterday_t += time_list[i].substring(13) + " - " + log_list[0] + "\n";
                    }
                }
                return null;
            }

            @Override
            protected void onPostExecute(Object o) {
                super.onPostExecute(o);
                textView.setText(today_t);
                textView.setMovementMethod(new ScrollingMovementMethod());
                textView2.setText(yesterday_t);
                textView2.setMovementMethod(new ScrollingMovementMethod());
                textView3.setText(byesterday_t);
                textView3.setMovementMethod(new ScrollingMovementMethod());
                textView4.setText(today);
                textView5.setText(yesterday);
                textView6.setText(byesterday);
            }
        }.execute();







    Button button = findViewById(R.id.Button_home);
        button.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v){
                Intent intent = new Intent();
                finish();
            }
        });
    }
}
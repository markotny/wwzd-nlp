import { Component, OnInit } from '@angular/core';
import { ResponseModel } from './core/models/response.model';
import { VisualizationHttpService } from './core/services/http/visualization-http.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'wwzd-frontend';
  data: any;

  constructor(private http: VisualizationHttpService<ResponseModel>) {}

  ngOnInit() {
    const response = this.http.get('check_party_affiliation');
    response.subscribe(
      (response) => {
        console.log(response);
      }
    );


    this.data = {
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      datasets: [
          {
              label: 'My First dataset',
              backgroundColor: '#42A5F5',
              borderColor: '#1E88E5',
              data: [65, 59, 80, 81, 56, 55, 40]
          },
          {
              label: 'My Second dataset',
              backgroundColor: '#9CCC65',
              borderColor: '#7CB342',
              data: [28, 48, 40, 19, 86, 27, 90]
          }
      ]
    }
  }
}


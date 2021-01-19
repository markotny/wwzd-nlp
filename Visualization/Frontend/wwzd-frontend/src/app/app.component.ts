import { Component, OnInit } from '@angular/core';
import { PersonResultModel } from './core/models/person-result.model';
import { QueryModel } from './core/models/query-model';
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
  people: Array<PersonResultModel>;
  query: string;

  constructor(private http: VisualizationHttpService<ResponseModel, QueryModel>) {}

  ngOnInit() {
    this.query = '';
  }

  private createPersons(response: Array<string>) {
    const people = Array<PersonResultModel>();

    for(const text of response) {
      const temp = text.split(':');
      let person = new PersonResultModel();
      person.probability = Number(temp[0]) * 100;
      person.party = temp[1].trim();
      person.name = temp[2].trim();
      person.speech = temp[3].trim();
      people.push(person);
    }
    return people
  }

  private createData() {
    const labels = Array<string>();
    const data = Array<number>();
    for(const person of this.people) {
      labels.push(person.name + ' ' + `(${person.party})`)
      data.push(person.probability);
    }
    this.data = {
      labels: labels,
      datasets: [
          {
            label: 'Prawdopodobieństwo wypowiedzi',
            backgroundColor: '#42A5F5',
            borderColor: '#1E88E5',
            data: data
          }
      ]
    }
  }

  makeRequest() {
    const queryModel = new QueryModel();
    queryModel.query = this.query;
    const response = this.http.post('check_party_affiliation', queryModel);
    response.subscribe(
      (response) => {
        this.people = this.createPersons(response.response);
        console.log(this.people);
        this.createData();
      }
    );
  }
}


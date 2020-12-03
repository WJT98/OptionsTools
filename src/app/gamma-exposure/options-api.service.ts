import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Options } from './options.model';
import { Subject } from 'rxjs';


import { API_URL } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class OptionsApiService {
	private options: Options[];
    private optionsUpdated = new Subject<Options[]>();
	constructor(private http: HttpClient) {
	}

	getOptionsUpdateListener() {
		return this.optionsUpdated.asObservable();
	}


	// GET list of public, future events
	getOptions(){
		this.http.get(`${API_URL}/tickers`)
        .subscribe((optionsData) => {
			//this.options= JSON.parse(optionsData.options.toString());
			this.options=JSON.parse(JSON.stringify(optionsData))
			console.log(JSON.stringify(optionsData))
			this.optionsUpdated.next([...this.options]);
		});


	}


}

//spread operator ...
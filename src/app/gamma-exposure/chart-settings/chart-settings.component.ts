import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';

import { ChartSettingsService } from '../chart.service';

@Component({
    selector: 'app-chart-settings',
    templateUrl: './chart-settings.component.html',
    styleUrls: ['./chart-settings.component.css'],
})
export class ChartSettingsComponent {
    constructor(public chartSettingsService: ChartSettingsService) {}

    onAddChart(form: NgForm) {
        if (form.invalid) {
            return;
        }
        this.chartSettingsService.addChart(form.value.ticker, form.value.timePeriod);
    }
}

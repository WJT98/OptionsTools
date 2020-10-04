import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { OptionsDataComponent } from './options-data/options-data.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { DashboardComponent } from './dashboard/dashboard.component';

// Add Material
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatToolbarModule } from '@angular/material/toolbar';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatDividerModule } from '@angular/material/divider';
import { MatListModule } from '@angular/material/list';
import { MatRippleModule } from '@angular/material/core';
import { MatButtonModule } from '@angular/material/button';




@NgModule({
    declarations: [
        AppComponent,
        HeaderComponent,
        OptionsDataComponent,
        SidebarComponent,
        DashboardComponent,
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        FlexLayoutModule,
        BrowserAnimationsModule,
        MatFormFieldModule,
        MatSelectModule,
        MatToolbarModule,
        MatInputModule,
        MatIconModule,
        MatSidenavModule,
        MatDividerModule,
        MatListModule,
        MatRippleModule,
        MatButtonModule
    ],
    providers: [],
    bootstrap: [AppComponent],
})
export class AppModule {}

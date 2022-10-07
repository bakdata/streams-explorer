package com.bakdata.kafka;

import com.opencsv.bean.CsvBindByName;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class AtmLocation {
    public AtmLocation() {
    }
    @CsvBindByName
    private Double lon;
    @CsvBindByName
    private Double lat;
    @CsvBindByName
    private String atmLabel;

}

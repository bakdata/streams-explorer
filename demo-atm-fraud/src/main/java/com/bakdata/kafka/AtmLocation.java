package com.bakdata.kafka;

import com.opencsv.bean.CsvBindByName;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class AtmLocation {
    @CsvBindByName
    private Double lon;
    @CsvBindByName
    private Double lat;
    @CsvBindByName
    private String atmLabel;

}

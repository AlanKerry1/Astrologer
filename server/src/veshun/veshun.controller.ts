import { Controller, Get, Post, Body, Patch, Param, Delete } from '@nestjs/common';
import { VeshunService } from './veshun.service';
import { GetTaroDto } from './dto/get-taro.dto';
import { GetHoroscopeDto } from './dto/get-horoscope.dto';
import { GetCompatibilityDto } from './dto/get-compatibility.dto';

@Controller('veshun')
export class VeshunController {
  constructor(private readonly veshunService: VeshunService) {}

  @Post("/taro")
  getTaro(@Body() getTaroDto: GetTaroDto) {
    return this.veshunService.getTaro(getTaroDto);
  }

  @Post("/horoscope")
  getHoroscope(@Body() getHoroscopeDto: GetHoroscopeDto) {
    return this.veshunService.getHoroscope(getHoroscopeDto);
  }

  @Post("/compatibility")
  getCompatibility(@Body() getCompatibilityDto: GetCompatibilityDto) {
    return this.veshunService.getCompatibility(getCompatibilityDto);
  }
}

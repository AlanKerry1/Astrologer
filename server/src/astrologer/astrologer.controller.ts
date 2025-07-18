import { Controller, Get, Post, Body, Patch, Param, Delete } from '@nestjs/common';
import { AstrologerService } from './astrologer.service';
import { GetTaroDto } from './dto/get-taro.dto';
import { GetHoroscopeDto } from './dto/get-horoscope.dto';
import { GetCompatibilityDto } from './dto/get-compatibility.dto';

@Controller('astrologer')
export class AstrologerController {
  constructor(private readonly astrologerService: AstrologerService) {}

  @Post("/taro")
  getTaro(@Body() getTaroDto: GetTaroDto) {
    return this.astrologerService.getTaro(getTaroDto);
  }

  @Post("/horoscope")
  getHoroscope(@Body() getHoroscopeDto: GetHoroscopeDto) {
    return this.astrologerService.getHoroscope(getHoroscopeDto);
  }

  @Post("/compatibility")
  getCompatibility(@Body() getCompatibilityDto: GetCompatibilityDto) {
    return this.astrologerService.getCompatibility(getCompatibilityDto);
  }
}

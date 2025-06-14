import { Injectable } from '@nestjs/common';
import { OpenaiService } from './openai/openai.service';
import { GetTaroDto } from './dto/get-taro.dto';
import { getCompatibilityPrompt, getHoroscopePrompt, getTaroPrompt } from 'src/veshun/prompts';
import { GetHoroscopeDto } from './dto/get-horoscope.dto';
import { GetCompatibilityDto } from './dto/get-compatibility.dto';

@Injectable()
export class VeshunService {

  constructor(private readonly openaiService: OpenaiService) {}

  async getTaro(getTaroDto: GetTaroDto) {
    const prompt = getTaroPrompt(getTaroDto);
    return await this.openaiService.askGpt(prompt);
  }

  async getHoroscope(getHoroscopeDto: GetHoroscopeDto) {
    const prompt = getHoroscopePrompt(getHoroscopeDto);
    return await this.openaiService.askGpt(prompt);
  }

  async getCompatibility(getCompatibilityDto: GetCompatibilityDto) {
    const prompt = getCompatibilityPrompt(getCompatibilityDto);
    return await this.openaiService.askGpt(prompt);
  }
}

import { Injectable } from '@nestjs/common';
import OpenAIApi from 'openai';

const MODEL = 'gpt-4o-mini';

@Injectable()
export class OpenaiService {
  constructor(private readonly openai: OpenAIApi) {}

  async askGpt(prompt) {
    const chatCompletion = await this.openai.chat.completions.create({
      model: MODEL,
      messages: [{ role: 'user', content: prompt }],
      temperature: 1,
    });
    return chatCompletion.choices[0].message.content;
  }
}

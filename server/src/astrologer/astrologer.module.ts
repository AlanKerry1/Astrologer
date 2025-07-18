import { Module } from '@nestjs/common';
import { AstrologerService } from './astrologer.service';
import { AstrologerController } from './astrologer.controller';
import { OpenaiModule } from './openai/openai.module';
import { OpenaiService } from './openai/openai.service';
import { ConfigModule, ConfigService } from '@nestjs/config';
import OpenAI from 'openai';

@Module({
  imports: [OpenaiModule, ConfigModule.forRoot()],
  controllers: [AstrologerController],
  providers: [AstrologerService, OpenaiService,
    {
      provide: OpenAI,
      useFactory: (configService: ConfigService) => {
        const apiKey = configService.get<string>("AI_KEY");
        return new OpenAI({apiKey});
      },
      inject: [ConfigService]
    },
  ],
})
export class AstrologerModule {}

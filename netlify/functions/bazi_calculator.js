// Bazi calculation utilities for JavaScript
// Implements traditional Chinese calendar calculations

class BaziCalculator {
  constructor() {
    this.gans = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"];
    this.zhis = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"];
    
    // Reference point: 1984-02-04 (甲子年甲寅月甲子日甲子时)
    this.referenceDate = new Date(1984, 1, 4); // February 4, 1984
    this.referenceDayCount = Math.floor(this.referenceDate.getTime() / (24 * 60 * 60 * 1000));
  }

  // Calculate day count from a reference point
  getDayCount(date) {
    return Math.floor(date.getTime() / (24 * 60 * 60 * 1000));
  }

  // Get Ganzhi for year based on solar calendar
  getYearGanzhi(year) {
    // Spring begins (立春) roughly around Feb 4th, so we use solar year
    // Year cycle: 60-year cycle, with 1984 being 甲子 (index 0)
    const yearOffset = year - 1984;
    const ganIndex = (yearOffset % 10 + 10) % 10;
    const zhiIndex = (yearOffset % 12 + 12) % 12;
    return [this.gans[ganIndex], this.zhis[zhiIndex]];
  }

  // Get Ganzhi for month (depends on year and month)
  getMonthGanzhi(year, month) {
    // Month calculation is complex and depends on solar terms
    // Simplified version: each year starts with different month Gan
    const [yearGan] = this.getYearGanzhi(year);
    const yearGanIndex = this.gans.indexOf(yearGan);
    
    // First month (寅月) Gan depends on year Gan
    // 甲己 years start with 丙寅, 乙庚 years start with 戊寅, etc.
    const monthGanStarts = [2, 4, 6, 8, 0]; // 丙戊庚壬甲
    const startGanIndex = monthGanStarts[Math.floor(yearGanIndex / 2)];
    
    // Month 1=寅(2), 2=卯(3), etc. February is 寅月
    const monthZhiIndex = (month + 1) % 12; // Feb=2(寅), Mar=3(卯), etc.
    const monthGanIndex = (startGanIndex + month - 1) % 10;
    
    return [this.gans[monthGanIndex], this.zhis[monthZhiIndex]];
  }

  // Get Ganzhi for day (continuous 60-day cycle)
  getDayGanzhi(date) {
    const dayCount = this.getDayCount(date);
    const dayOffset = dayCount - this.referenceDayCount;
    
    const ganIndex = (dayOffset % 10 + 10) % 10;
    const zhiIndex = (dayOffset % 12 + 12) % 12;
    
    return [this.gans[ganIndex], this.zhis[zhiIndex]];
  }

  // Get Ganzhi for hour (depends on day and hour)
  getHourGanzhi(date, hour) {
    const [dayGan] = this.getDayGanzhi(date);
    const dayGanIndex = this.gans.indexOf(dayGan);
    
    // Hour Gan depends on day Gan
    // 甲己 days start with 甲子时, 乙庚 days start with 丙子时, etc.
    const hourGanStarts = [0, 2, 4, 6, 8]; // 甲丙戊庚壬
    const startGanIndex = hourGanStarts[Math.floor(dayGanIndex / 2)];
    
    // Hour mapping: 23-1=子, 1-3=丑, 3-5=寅, etc.
    const hourZhiIndex = Math.floor((hour + 1) / 2) % 12;
    const hourGanIndex = (startGanIndex + hourZhiIndex) % 10;
    
    return [this.gans[hourGanIndex], this.zhis[hourZhiIndex]];
  }

  // Calculate 大运 (luck pillar) based on year Gan and gender
  calculateDayun(yearGan, monthGan, monthZhi, isFemal) {
    const yearGanIndex = this.gans.indexOf(yearGan);
    const isYangYear = yearGanIndex % 2 === 0;
    
    // Direction depends on year parity and gender
    const direction = (isFemal ? !isYangYear : isYangYear) ? 1 : -1;
    
    // Random age periods (simplified)
    const agePeriods = Math.floor(Math.random() * 5) + 2;
    
    let ganIndex = this.gans.indexOf(monthGan);
    let zhiIndex = this.zhis.indexOf(monthZhi);
    
    for (let i = 0; i < agePeriods; i++) {
      ganIndex = (ganIndex + direction + 10) % 10;
      zhiIndex = (zhiIndex + direction + 12) % 12;
    }
    
    return [this.gans[ganIndex], this.zhis[zhiIndex]];
  }

  // Generate Bazi from birth date
  generateFromBirthDate(year, month, day, hour, isFemale = false, advancedMode = false) {
    const date = new Date(year, month - 1, day); // month is 0-indexed in JS
    
    const yearGZ = this.getYearGanzhi(year);
    const monthGZ = this.getMonthGanzhi(year, month);
    const dayGZ = this.getDayGanzhi(date);
    const hourGZ = this.getHourGanzhi(date, hour);
    
    const chart = {
      year_gan: yearGZ[0], year_zhi: yearGZ[1],
      month_gan: monthGZ[0], month_zhi: monthGZ[1],
      day_gan: dayGZ[0], day_zhi: dayGZ[1],
      hour_gan: hourGZ[0], hour_zhi: hourGZ[1],
      gans: [yearGZ[0], monthGZ[0], dayGZ[0], hourGZ[0]],
      zhis: [yearGZ[1], monthGZ[1], dayGZ[1], hourGZ[1]],
      date_info: `${year}年${month}月${day}日${hour}时`,
      is_female: isFemale,
      advanced_mode: advancedMode
    };
    
    if (advancedMode) {
      const dayunGZ = this.calculateDayun(yearGZ[0], monthGZ[0], monthGZ[1], isFemale);
      const currentYear = new Date().getFullYear();
      const liunianGZ = this.getYearGanzhi(currentYear);
      
      chart.dayun_gan = dayunGZ[0];
      chart.dayun_zhi = dayunGZ[1];
      chart.liunian_gan = liunianGZ[0];
      chart.liunian_zhi = liunianGZ[1];
      chart.gans = [...chart.gans, dayunGZ[0], liunianGZ[0]];
      chart.zhis = [...chart.zhis, dayunGZ[1], liunianGZ[1]];
      chart.current_year = currentYear;
    }
    
    return chart;
  }

  // Generate random Bazi (existing functionality)
  generateRandom(advancedMode = false) {
    const year = 1950 + Math.floor(Math.random() * 70); // 1950-2020
    const month = 1 + Math.floor(Math.random() * 12);   // 1-12
    const day = 1 + Math.floor(Math.random() * 28);     // 1-28
    const hour = Math.floor(Math.random() * 24);        // 0-23
    const isFemale = Math.random() > 0.5;
    
    return this.generateFromBirthDate(year, month, day, hour, isFemale, advancedMode);
  }
}

module.exports = BaziCalculator;
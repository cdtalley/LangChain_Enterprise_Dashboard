/**
 * Demo Data Generator - TypeScript Port
 * Generates realistic demo datasets for various industries
 */

export interface DatasetInfo {
  icon: string;
  description: string;
  size: string;
}

export interface HealthcareRecord {
  patient_id: string;
  age: number;
  gender: string;
  bmi: number;
  blood_pressure_systolic: number;
  blood_pressure_diastolic: number;
  cholesterol: number;
  glucose: number;
  condition: string;
  medication: string;
  visit_date: string;
  cost: number;
  readmission_risk: number;
}

export interface FinanceRecord {
  transaction_id: string;
  customer_id: string;
  date: string;
  transaction_type: string;
  category: string;
  merchant: string;
  amount: number;
  currency: string;
  is_fraud: number;
  account_balance: number;
  credit_score: number;
}

export interface EcommerceRecord {
  order_id: string;
  customer_id: string;
  product: string;
  category: string;
  order_date: string;
  quantity: number;
  unit_price: number;
  total_amount: number;
  region: string;
  payment_method: string;
  shipping_cost: number;
  discount: number;
  returned: number;
}

export interface MarketingRecord {
  campaign_id: string;
  campaign_name: string;
  channel: string;
  region: string;
  date: string;
  impressions: number;
  clicks: number;
  conversions: number;
  spend: number;
  revenue: number;
  ctr: number;
  conversion_rate: number;
  roas: number;
}

export interface HRRecord {
  employee_id: string;
  name: string;
  department: string;
  job_title: string;
  location: string;
  hire_date: string;
  age: number;
  years_experience: number;
  salary: number;
  performance_score: number;
  satisfaction_score: number;
  projects_completed: number;
  training_hours: number;
  promoted: number;
  left_company: number;
}

class DemoDataGenerator {
  private seed: number;
  private randomFn: () => number = () => Math.random();

  constructor(seed: number = 42) {
    this.seed = seed;
    this.seedRandom();
  }

  private seedRandom(): void {
    // Simple seeded random number generator
    let seed = this.seed;
    this.randomFn = () => {
      seed = (seed * 9301 + 49297) % 233280;
      return seed / 233280;
    };
  }

  private random(): number {
    return this.randomFn ? this.randomFn() : Math.random();
  }

  private randomInt(min: number, max: number): number {
    return Math.floor(this.random() * (max - min + 1)) + min;
  }

  private randomChoice<T>(array: T[]): T {
    return array[Math.floor(this.random() * array.length)];
  }

  private randomNormal(mean: number, std: number): number {
    const u1 = this.random();
    const u2 = this.random();
    const z0 = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
    return z0 * std + mean;
  }

  private randomLognormal(mean: number, std: number): number {
    return Math.exp(this.randomNormal(Math.log(mean), std));
  }

  private randomPoisson(lambda: number): number {
    let k = 0;
    let p = 1;
    const L = Math.exp(-lambda);
    do {
      k++;
      p *= this.random();
    } while (p > L);
    return k - 1;
  }

  private clamp(value: number, min: number, max: number): number {
    return Math.max(min, Math.min(max, value));
  }

  private formatDate(date: Date): string {
    return date.toISOString().split('T')[0];
  }

  generateHealthcareData(nRecords: number = 1000): HealthcareRecord[] {
    const conditions = ['Hypertension', 'Diabetes', 'Asthma', 'Arthritis', 'Heart Disease', 'Obesity'];
    const medications = ['Metformin', 'Lisinopril', 'Albuterol', 'Ibuprofen', 'Aspirin', 'Atorvastatin'];
    const conditionProbs = [0.25, 0.20, 0.15, 0.15, 0.15, 0.10];
    
    const records: HealthcareRecord[] = [];
    const startDate = new Date('2023-01-01');

    for (let i = 1; i <= nRecords; i++) {
      const conditionIdx = this.weightedChoice(conditionProbs);
      const visitDate = new Date(startDate);
      visitDate.setDate(visitDate.getDate() + i - 1);

      records.push({
        patient_id: `PAT-${i.toString().padStart(4, '0')}`,
        age: this.clamp(Math.round(this.randomNormal(45, 15)), 18, 90),
        gender: this.randomChoice(['M', 'F']),
        bmi: Math.round(this.clamp(this.randomNormal(26, 5), 18, 40) * 10) / 10,
        blood_pressure_systolic: this.clamp(Math.round(this.randomNormal(120, 15)), 90, 180),
        blood_pressure_diastolic: this.clamp(Math.round(this.randomNormal(80, 10)), 60, 120),
        cholesterol: this.clamp(Math.round(this.randomNormal(200, 40)), 100, 300),
        glucose: this.clamp(Math.round(this.randomNormal(100, 20)), 70, 200),
        condition: conditions[conditionIdx],
        medication: this.randomChoice(medications),
        visit_date: this.formatDate(visitDate),
        cost: Math.round(this.randomLognormal(5, 1) * 100) / 100,
        readmission_risk: this.random() < 0.15 ? 1 : 0,
      });
    }

    return records;
  }

  generateFinanceData(nRecords: number = 1000): FinanceRecord[] {
    const transactionTypes = ['Purchase', 'Transfer', 'Deposit', 'Withdrawal', 'Payment', 'Refund'];
    const categories = ['Groceries', 'Restaurants', 'Shopping', 'Transport', 'Bills', 'Entertainment', 'Healthcare'];
    const merchants = ['Amazon', 'Walmart', 'Target', 'Starbucks', 'Shell', 'AT&T', 'Netflix', 'CVS'];
    const typeProbs = [0.40, 0.15, 0.15, 0.10, 0.15, 0.05];

    const records: FinanceRecord[] = [];
    const startDate = new Date('2024-01-01');

    for (let i = 1; i <= nRecords; i++) {
      const typeIdx = this.weightedChoice(typeProbs);
      const date = new Date(startDate);
      date.setHours(date.getHours() + i - 1);

      records.push({
        transaction_id: `TXN-${i.toString().padStart(6, '0')}`,
        customer_id: `CUST-${this.randomInt(1000, 9999)}`,
        date: date.toISOString(),
        transaction_type: transactionTypes[typeIdx],
        category: this.randomChoice(categories),
        merchant: this.randomChoice(merchants),
        amount: Math.round(this.randomLognormal(3.5, 1.2) * 100) / 100,
        currency: 'USD',
        is_fraud: this.random() < 0.03 ? 1 : 0,
        account_balance: Math.round(this.randomNormal(5000, 2000) * 100) / 100,
        credit_score: this.clamp(Math.round(this.randomNormal(720, 50)), 300, 850),
      });
    }

    return records;
  }

  generateEcommerceData(nRecords: number = 1000): EcommerceRecord[] {
    const products = ['Laptop', 'Smartphone', 'Headphones', 'Tablet', 'Smartwatch', 'Camera', 'Speaker', 'Monitor'];
    const categories = ['Electronics', 'Computers', 'Audio', 'Mobile', 'Wearables', 'Photography', 'Accessories'];
    const regions = ['North', 'South', 'East', 'West', 'Central'];
    const paymentMethods = ['Credit Card', 'Debit Card', 'PayPal', 'Apple Pay'];
    const shippingCosts = [0, 5.99, 9.99, 14.99];
    const shippingProbs = [0.3, 0.4, 0.2, 0.1];
    const discounts = [0, 0.05, 0.10, 0.15, 0.20];
    const discountProbs = [0.5, 0.2, 0.15, 0.10, 0.05];

    const records: EcommerceRecord[] = [];
    const startDate = new Date('2024-01-01');

    for (let i = 1; i <= nRecords; i++) {
      const date = new Date(startDate);
      date.setHours(date.getHours() + i - 1);
      
      const quantity = this.clamp(this.randomPoisson(2), 1, 10);
      const unitPrice = Math.round(this.randomLognormal(4, 1) * 100) / 100;
      const discount = discounts[this.weightedChoice(discountProbs)];
      const shippingCost = shippingCosts[this.weightedChoice(shippingProbs)];
      const totalAmount = Math.round((quantity * unitPrice * (1 - discount) + shippingCost) * 100) / 100;

      records.push({
        order_id: `ORD-${i.toString().padStart(6, '0')}`,
        customer_id: `CUST-${this.randomInt(1000, 9999)}`,
        product: this.randomChoice(products),
        category: this.randomChoice(categories),
        order_date: date.toISOString(),
        quantity,
        unit_price: unitPrice,
        total_amount: totalAmount,
        region: this.randomChoice(regions),
        payment_method: this.randomChoice(paymentMethods),
        shipping_cost: shippingCost,
        discount,
        returned: this.random() < 0.08 ? 1 : 0,
      });
    }

    return records;
  }

  generateMarketingData(nRecords: number = 1000): MarketingRecord[] {
    const channels = ['Email', 'Social Media', 'Search Ads', 'Display Ads', 'TV', 'Radio', 'Print'];
    const campaigns = ['Summer Sale', 'Black Friday', 'Holiday Special', 'New Product Launch', 'Brand Awareness'];
    const regions = ['North America', 'Europe', 'Asia', 'South America', 'Oceania'];

    const records: MarketingRecord[] = [];
    const startDate = new Date('2024-01-01');

    for (let i = 1; i <= nRecords; i++) {
      const date = new Date(startDate);
      date.setDate(date.getDate() + i - 1);

      const impressions = this.clamp(this.randomPoisson(10000), 1000, 50000);
      const ctr = this.random() * 0.04 + 0.01; // 1-5% CTR
      const clicks = Math.floor(impressions * ctr);
      const conversionRate = this.random() * 0.08 + 0.02; // 2-10% conversion
      const conversions = Math.floor(clicks * conversionRate);
      const spend = Math.round(this.randomLognormal(6, 1) * 100) / 100;
      const revenue = Math.round(conversions * (this.random() * 150 + 50) * 100) / 100;
      const roas = spend > 0 ? Math.round((revenue / spend) * 100) / 100 : 0;

      records.push({
        campaign_id: `CAMP-${i.toString().padStart(4, '0')}`,
        campaign_name: this.randomChoice(campaigns),
        channel: this.randomChoice(channels),
        region: this.randomChoice(regions),
        date: this.formatDate(date),
        impressions,
        clicks,
        conversions,
        spend,
        revenue,
        ctr: Math.round(ctr * 10000) / 100,
        conversion_rate: Math.round(conversionRate * 10000) / 100,
        roas,
      });
    }

    return records;
  }

  generateHRData(nRecords: number = 1000): HRRecord[] {
    const departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations', 'Product'];
    const jobTitles = ['Junior', 'Mid-Level', 'Senior', 'Lead', 'Manager', 'Director', 'VP'];
    const locations = ['New York', 'San Francisco', 'Austin', 'Seattle', 'Boston', 'Remote'];
    const titleMultipliers: Record<string, number> = {
      'Junior': 1.0,
      'Mid-Level': 1.3,
      'Senior': 1.6,
      'Lead': 2.0,
      'Manager': 2.5,
      'Director': 3.5,
      'VP': 5.0,
    };

    const records: HRRecord[] = [];
    const startDate = new Date('2015-01-01');

    for (let i = 1; i <= nRecords; i++) {
      const hireDate = new Date(startDate);
      hireDate.setDate(hireDate.getDate() + i - 1);
      
      const yearsExperience = this.clamp(Math.round(this.randomNormal(8, 5) * 10) / 10, 0, 30);
      const jobTitle = this.randomChoice(jobTitles);
      const baseSalary = 50000 + yearsExperience * 5000;
      const salary = Math.round(baseSalary * titleMultipliers[jobTitle]);

      records.push({
        employee_id: `EMP-${i.toString().padStart(5, '0')}`,
        name: `Employee ${i}`,
        department: this.randomChoice(departments),
        job_title: jobTitle,
        location: this.randomChoice(locations),
        hire_date: this.formatDate(hireDate),
        age: this.clamp(Math.round(this.randomNormal(35, 10)), 22, 65),
        years_experience: yearsExperience,
        salary,
        performance_score: Math.round(this.clamp(this.randomNormal(85, 10), 60, 100) * 10) / 10,
        satisfaction_score: Math.round(this.clamp(this.randomNormal(7.5, 1.5), 1, 10) * 10) / 10,
        projects_completed: this.clamp(this.randomPoisson(5), 0, 20),
        training_hours: this.clamp(this.randomPoisson(20), 0, 100),
        promoted: this.random() < 0.3 ? 1 : 0,
        left_company: this.random() < 0.15 ? 1 : 0,
      });
    }

    return records;
  }

  private weightedChoice(weights: number[]): number {
    const total = weights.reduce((sum, w) => sum + w, 0);
    let random = this.random() * total;
    
    for (let i = 0; i < weights.length; i++) {
      random -= weights[i];
      if (random <= 0) {
        return i;
      }
    }
    
    return weights.length - 1;
  }

  getAvailableDatasets(): Record<string, DatasetInfo> {
    return {
      'Healthcare': {
        icon: '🏥',
        description: 'Patient records, vitals, conditions, medications',
        size: '1000 records',
      },
      'Finance': {
        icon: '💳',
        description: 'Transactions, fraud detection, customer data',
        size: '1000 records',
      },
      'E-commerce': {
        icon: '🛒',
        description: 'Sales, products, orders, customer behavior',
        size: '1000 records',
      },
      'Marketing': {
        icon: '📢',
        description: 'Campaigns, conversions, ROI, channel performance',
        size: '1000 records',
      },
      'HR': {
        icon: '👥',
        description: 'Employee data, performance, retention',
        size: '1000 records',
      },
    };
  }

  generateDataset(industry: string, nRecords: number = 1000): any[] {
    switch (industry) {
      case 'Healthcare':
        return this.generateHealthcareData(nRecords);
      case 'Finance':
        return this.generateFinanceData(nRecords);
      case 'E-commerce':
        return this.generateEcommerceData(nRecords);
      case 'Marketing':
        return this.generateMarketingData(nRecords);
      case 'HR':
        return this.generateHRData(nRecords);
      default:
        throw new Error(`Unknown industry: ${industry}`);
    }
  }
}

export default DemoDataGenerator;


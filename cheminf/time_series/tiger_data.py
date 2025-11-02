# Standalone Python Time Series Data Manager
import json
import os
from datetime import datetime, timedelta
import pickle
import random

class PythonTimeSeriesDB:
    """Pure Python time series data management - no external database required"""
    
    def __init__(self):
        self.data_dir = "time_series_data"
        self.experiments_file = os.path.join(self.data_dir, "experiments.json")
        self.series_data_dir = os.path.join(self.data_dir, "series")
        self.setup_storage()
        self.initialize_sample_data()
    
    def setup_storage(self):
        """Setup local file storage structure"""
        try:
            # Create directories if they don't exist
            os.makedirs(self.data_dir, exist_ok=True)
            os.makedirs(self.series_data_dir, exist_ok=True)
            
            # Create experiments file if it doesn't exist
            if not os.path.exists(self.experiments_file):
                with open(self.experiments_file, 'w') as f:
                    json.dump([], f)
            
            print("File-based time series storage initialized")
            
        except Exception as e:
            print(f"Storage setup failed: {e}")
    
    def setup_schema(self):
        """Setup TimescaleDB schema for time series data"""
        if not self.conn:
            return
        
        try:
            cursor = self.conn.cursor()
            
            # Create TimescaleDB extension (if not already created)
            cursor.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")
            
            # Create experiments table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS experiments (
                    experiment_id VARCHAR(50) PRIMARY KEY,
                    experiment_name VARCHAR(200),
                    description TEXT,
                    start_date TIMESTAMPTZ,
                    end_date TIMESTAMPTZ,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)
            
            # Create time series data table (hypertable)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS time_series_data (
                    timestamp TIMESTAMPTZ NOT NULL,
                    experiment_id VARCHAR(50) NOT NULL,
                    series_name VARCHAR(200),
                    parameter_name VARCHAR(100),
                    value DOUBLE PRECISION,
                    unit VARCHAR(20),
                    time_step INTEGER,
                    notes TEXT,
                    FOREIGN KEY (experiment_id) REFERENCES experiments(experiment_id)
                );
            """)
            
            # Convert to hypertable (TimescaleDB specific)
            try:
                cursor.execute("SELECT create_hypertable('time_series_data', 'timestamp', if_not_exists => TRUE);")
            except psycopg2.Error as e:
                # Hypertable may already exist
                if "already a hypertable" not in str(e):
                    print(f"Hypertable creation info: {e}")
            
            # Create index for faster queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_time_series_exp_param 
                ON time_series_data (experiment_id, parameter_name, timestamp);
            """)
            
            cursor.close()
            print("TimescaleDB schema setup completed")
            
        except Exception as e:
            print(f"Schema setup failed: {e}")
    
    def create_sample_time_series_data(self):
        """Create sample time series data in TigerGraph format"""
        # For demo purposes, we'll create mock data structure
        # In real implementation, this would insert into TigerGraph
        
        experiments = [
            {
                "experiment_id": "ASP-OPT-001",
                "experiment_name": "Aspirin Optimization",
                "description": "Temperature and pressure optimization for aspirin synthesis",
                "series": [
                    {
                        "series_id": "ASP-OPT-001-TEMP",
                        "parameter_name": "Temperature",
                        "unit": "°C",
                        "data_points": self.generate_temperature_series()
                    },
                    {
                        "series_id": "ASP-OPT-001-PRESS", 
                        "parameter_name": "Pressure",
                        "unit": "bar",
                        "data_points": self.generate_pressure_series()
                    },
                    {
                        "series_id": "ASP-OPT-001-PH",
                        "parameter_name": "pH", 
                        "unit": "",
                        "data_points": self.generate_ph_series()
                    },
                    {
                        "series_id": "ASP-OPT-001-YIELD",
                        "parameter_name": "Yield",
                        "unit": "%", 
                        "data_points": self.generate_yield_series()
                    }
                ]
            },
            {
                "experiment_id": "ASP-PUR-001",
                "experiment_name": "Aspirin Purification",
                "description": "Purification process optimization",
                "series": [
                    {
                        "series_id": "ASP-PUR-001-TEMP",
                        "parameter_name": "Temperature", 
                        "unit": "°C",
                        "data_points": self.generate_temperature_series(base_temp=65)
                    },
                    {
                        "series_id": "ASP-PUR-001-PURITY",
                        "parameter_name": "Purity",
                        "unit": "%",
                        "data_points": self.generate_purity_series()
                    }
                ]
            },
            {
                "experiment_id": "ASP-SID-001", 
                "experiment_name": "Side Products Analysis",
                "description": "Analysis of side product formation",
                "series": [
                    {
                        "series_id": "ASP-SID-001-TEMP",
                        "parameter_name": "Temperature",
                        "unit": "°C", 
                        "data_points": self.generate_temperature_series(base_temp=75)
                    },
                    {
                        "series_id": "ASP-SID-001-SIDE",
                        "parameter_name": "Side Products",
                        "unit": "ppm",
                        "data_points": self.generate_side_products_series()
                    }
                ]
            }
        ]
        
        return experiments
    
    def generate_temperature_series(self, base_temp=85):
        """Generate temperature time series data"""
        import random
        data_points = []
        
        for step in range(100):
            # Temperature ramps up then stabilizes
            if step < 20:
                temp = base_temp + (step * 0.5) + random.gauss(0, 2)
            elif step < 80:
                temp = base_temp + 10 + random.gauss(0, 1)
            else:
                temp = base_temp + 12 + random.gauss(0, 0.5)
            
            data_points.append({
                "time_step": step + 1,
                "timestamp": f"2024-10-15T09:{(step * 5) // 60:02d}:{(step * 5) % 60:02d}",
                "value": round(temp, 2)
            })
        
        return data_points
    
    def generate_pressure_series(self):
        """Generate pressure time series data"""
        import random
        data_points = []
        
        for step in range(100):
            # Pressure increases gradually
            pressure = 1.0 + (step / 100 * 0.5) + random.gauss(0, 0.05)
            
            data_points.append({
                "time_step": step + 1,
                "timestamp": f"2024-10-15T09:{(step * 5) // 60:02d}:{(step * 5) % 60:02d}",
                "value": round(pressure, 3)
            })
        
        return data_points
    
    def generate_ph_series(self):
        """Generate pH time series data"""
        import random
        data_points = []
        
        for step in range(100):
            # pH decreases over time (acid formation)
            ph = 4.0 - (step / 100 * 1.5) + random.gauss(0, 0.1)
            
            data_points.append({
                "time_step": step + 1,
                "timestamp": f"2024-10-15T09:{(step * 5) // 60:02d}:{(step * 5) % 60:02d}",
                "value": round(ph, 2)
            })
        
        return data_points
    
    def generate_yield_series(self):
        """Generate yield time series data"""
        import random
        data_points = []
        
        for step in range(100):
            # Yield improves over time then plateaus
            if step < 60:
                yield_val = 50 + (step / 60 * 45) + random.gauss(0, 3)
            else:
                yield_val = 95 + random.gauss(0, 1)
            
            data_points.append({
                "time_step": step + 1,
                "timestamp": f"2024-10-15T09:{(step * 5) // 60:02d}:{(step * 5) % 60:02d}",
                "value": round(yield_val, 2)
            })
        
        return data_points
    
    def generate_purity_series(self):
        """Generate purity time series data"""
        import random
        data_points = []
        
        for step in range(100):
            # Purity improves over time
            purity = 85 + (step / 100 * 12) + random.gauss(0, 1.5)
            
            data_points.append({
                "time_step": step + 1,
                "timestamp": f"2024-10-15T09:{(step * 5) // 60:02d}:{(step * 5) % 60:02d}",
                "value": round(min(purity, 99.9), 2)
            })
        
        return data_points
    
    def generate_side_products_series(self):
        """Generate side products time series data"""
        import random
        data_points = []
        
        for step in range(100):
            # Side products decrease over time with optimization
            if step < 40:
                side_products = 800 - (step * 15) + random.gauss(0, 50)
            else:
                side_products = 200 + random.gauss(0, 20)
            
            data_points.append({
                "time_step": step + 1,
                "timestamp": f"2024-10-15T09:{(step * 5) // 60:02d}:{(step * 5) % 60:02d}",
                "value": round(max(side_products, 0), 1)
            })
        
        return data_points
    
    def get_experiments(self):
        """Get all experiments with time series data"""
        if self.conn:
            try:
                # In real implementation, this would query TigerGraph
                # query = "SELECT * FROM Experiment"
                # return self.conn.runQuery(query)
                pass
            except Exception as e:
                print(f"TigerGraph query failed: {e}")
        
        # Return mock data for demo
        return self.create_sample_time_series_data()
    
    def get_time_series_data(self, experiment_id, parameters=None):
        """Get time series data for specific experiment and parameters"""
        experiments = self.get_experiments()
        
        for exp in experiments:
            if exp["experiment_id"] == experiment_id:
                if parameters:
                    # Filter by selected parameters
                    filtered_series = [
                        series for series in exp["series"] 
                        if series["parameter_name"] in parameters
                    ]
                    return {"experiment": exp, "series": filtered_series}
                else:
                    return {"experiment": exp, "series": exp["series"]}
        
        return None
    
    def get_series_info(self, experiment_id):
        """Get information about available series for an experiment"""
        experiments = self.get_experiments()
        
        for exp in experiments:
            if exp["experiment_id"] == experiment_id:
                series_info = []
                for series in exp["series"]:
                    series_info.append({
                        "parameter_name": series["parameter_name"],
                        "unit": series["unit"],
                        "data_points": len(series["data_points"]),
                        "start_time": series["data_points"][0]["timestamp"] if series["data_points"] else "",
                        "end_time": series["data_points"][-1]["timestamp"] if series["data_points"] else ""
                    })
                return series_info
        
        return []

# Global TigerGraph connection instance
tiger_conn = TigerDataConnection()
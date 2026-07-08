from app.dashboard.repository import DashboardRepository


class DashboardService:

    @staticmethod
    def get_dashboard(user_id):
        try:
            # 1. Fetch general summary
            summary_row = DashboardRepository.get_summary(user_id)
            if summary_row:
                income = float(summary_row[0]) if summary_row[0] is not None else 0.0
                expense = float(summary_row[1]) if summary_row[1] is not None else 0.0
                balance = income - expense
                movements_count = int(summary_row[2]) if summary_row[2] is not None else 0
            else:
                income = 0.0
                expense = 0.0
                balance = 0.0
                movements_count = 0

            summary = {
                "balance": balance,
                "income": income,
                "expense": expense,
                "movements": movements_count
            }

            # 2. Fetch last 5 movements
            last_mov_rows = DashboardRepository.get_last_movements(user_id)
            last_movements = []
            for row in last_mov_rows:
                m_date = row[3]
                if m_date and hasattr(m_date, "strftime"):
                    formatted_date = m_date.strftime("%Y-%m-%d")
                else:
                    formatted_date = str(m_date) if m_date else ""

                last_movements.append({
                    "id": row[0],
                    "description": row[1],
                    "amount": float(row[2]) if row[2] is not None else 0.0,
                    "movement_date": formatted_date,
                    "category_name": row[4],
                    "type": row[5]
                })

            # 3. Fetch expenses by category
            expenses_rows = DashboardRepository.get_expenses_by_category(user_id)
            expenses_by_category = []
            for row in expenses_rows:
                expenses_by_category.append({
                    "category": row[0],
                    "total": float(row[1]) if row[1] is not None else 0.0
                })

            # 4. Fetch current month balance
            monthly_row = DashboardRepository.get_monthly_balance(user_id)
            if monthly_row:
                monthly_income = float(monthly_row[0]) if monthly_row[0] is not None else 0.0
                monthly_expense = float(monthly_row[1]) if monthly_row[1] is not None else 0.0
                monthly_balance_val = monthly_income - monthly_expense
            else:
                monthly_income = 0.0
                monthly_expense = 0.0
                monthly_balance_val = 0.0

            monthly_balance = {
                "income": monthly_income,
                "expense": monthly_expense,
                "balance": monthly_balance_val
            }

            return {
                "summary": summary,
                "last_movements": last_movements,
                "expenses_by_category": expenses_by_category,
                "monthly_balance": monthly_balance
            }, 200

        except Exception as e:
            return {
                "message": "Error al obtener la información del dashboard.",
                "error": str(e)
            }, 500

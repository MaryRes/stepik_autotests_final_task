# data/known_issues.py
from datetime import datetime, timedelta


class KnownIssues:
    ISSUES = {
        "incorrect_product_name_bug": {
            "url": "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer7",
            "test_case": "test_guest_can_add_product_to_basket",
            "expected_incorrect_value": "Coders at Work book",
            "expected_correct_value": "Coders at Work",
            "name": "incorrect_product_name_bug",
            "description": "After clicking 'add to basket', "
                           "product name in basket is 'Coders at Work book' but expected to be 'Coders at Work'",
            "severity": "low",  # critical, high, medium, low
            "reported_date": "2025-08-17",
            "expected_fix_date": "2025-09-09",
            "status": "open",  # open, in_progress, fixed, wont_fix
            "reason": "Product team decided this is expected behavior",
            "decision_by": "product_manager@company.com",
            "decision_date": "2025-08-19",
            "affected_users": "All users seeing English version",
            "workaround": "Ignore the extra 'book' in product name"
                                      }


    }

    @ classmethod
    def get_urgent_issues(cls):
        """Получить срочные issues"""
        return {k: v for k, v in cls.ISSUES.items() if v['severity'] in ['critical', 'high']}

    @classmethod
    def get_stale_issues(cls, days=30):
        """Получить старые нерешенные issues"""
        stale_date = datetime.now() - timedelta(days=days)
        stale_issues = {}

        for issue_name, issue_data in cls.ISSUES.items():
            if issue_data['status'] == 'open':
                reported_date = datetime.strptime(issue_data['reported_date'], '%Y-%m-%d')
                if reported_date < stale_date:
                    stale_issues[issue_name] = issue_data

        return stale_issues

    @classmethod
    def get_active_issues(cls):
        """Получить все активные issues"""
        return [k for k, v in cls.ISSUES.items() if v['status'] in ['open', 'in_progress']]


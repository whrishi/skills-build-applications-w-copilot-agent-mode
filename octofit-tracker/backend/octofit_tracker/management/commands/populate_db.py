from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create users
        users = [
            User(_id=ObjectId(), username='thundergod', email='thundergod@mhigh.edu', password='password1'),
            User(_id=ObjectId(), username='metalgeek', email='metalgeek@mhigh.edu', password='password2'),
            User(_id=ObjectId(), username='zerocool', email='zerocool@mhigh.edu', password='password3'),
            User(_id=ObjectId(), username='crashoverride', email='crashoverride@mhigh.edu', password='password4'),
            User(_id=ObjectId(), username='sleeptoken', email='sleeptoken@mhigh.edu', password='password5'),
        ]
        User.objects.bulk_create(users)

        # Log user creation
        for user in users:
            self.stdout.write(f"Created user: {user.username} ({user.email})")

        # Create teams
        team1 = Team(_id=ObjectId(), name='Blue Team')
        team2 = Team(_id=ObjectId(), name='Gold Team')
        team1.save()
        team2.save()
        team1.members.add(users[0], users[1])
        team2.members.add(users[2], users[3], users[4])

        # Log team creation
        self.stdout.write(f"Created team: {team1.name} with members {[user.username for user in team1.members.all()]}")
        self.stdout.write(f"Created team: {team2.name} with members {[user.username for user in team2.members.all()]}")

        # Create activities
        activities = [
            Activity(_id=ObjectId(), user=users[0], activity_type='Cycling', duration=timedelta(hours=1)),
            Activity(_id=ObjectId(), user=users[1], activity_type='Crossfit', duration=timedelta(hours=2)),
            Activity(_id=ObjectId(), user=users[2], activity_type='Running', duration=timedelta(hours=1, minutes=30)),
            Activity(_id=ObjectId(), user=users[3], activity_type='Strength', duration=timedelta(minutes=30)),
            Activity(_id=ObjectId(), user=users[4], activity_type='Swimming', duration=timedelta(hours=1, minutes=15)),
        ]
        Activity.objects.bulk_create(activities)

        # Log activity creation
        for activity in activities:
            self.stdout.write(f"Created activity: {activity.activity_type} for user {activity.user.username}")

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(_id=ObjectId(), user=users[0], score=100),
            Leaderboard(_id=ObjectId(), user=users[1], score=90),
            Leaderboard(_id=ObjectId(), user=users[2], score=95),
            Leaderboard(_id=ObjectId(), user=users[3], score=85),
            Leaderboard(_id=ObjectId(), user=users[4], score=80),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Log leaderboard creation
        for entry in leaderboard_entries:
            self.stdout.write(f"Created leaderboard entry: {entry.user.username} with score {entry.score}")

        # Create workouts
        workouts = [
            Workout(_id=ObjectId(), name='Cycling Training', description='Training for a road cycling event'),
            Workout(_id=ObjectId(), name='Crossfit', description='Training for a crossfit competition'),
            Workout(_id=ObjectId(), name='Running Training', description='Training for a marathon'),
            Workout(_id=ObjectId(), name='Strength Training', description='Training for strength'),
            Workout(_id=ObjectId(), name='Swimming Training', description='Training for a swimming competition'),
        ]
        Workout.objects.bulk_create(workouts)

        # Log workout creation
        for workout in workouts:
            self.stdout.write(f"Created workout: {workout.name} ({workout.description})")

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
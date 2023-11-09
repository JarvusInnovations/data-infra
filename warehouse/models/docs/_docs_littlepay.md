Documentation related to Littlepay data schema

{% docs lp_participant_id %}
Littlepay identifier for the participant (transit agency) associated with this entity or event.
{% enddocs %}

{% docs lp_net_micropayment_amount_dollars %}
Sum of the `charge_amount` values for all micropayments in this aggregation.
If there are credit (pre-settlement refund) micropayments in the aggregation,
the value of those will have been subtracted from this total because they have
negative `charge_amount` values.
Post-settlement refunds will not be reflected since they are not recorded in the micropayments table.
{% enddocs %}

{% docs lp_total_nominal_amount_dollars %}
Sum of the `nominal_amount` (unadjusted) values for all micropayments in this aggregation.
This will not reflect pre-settlement refunds or micropayment adjustments.
{% enddocs %}

{% docs lp_mp_latest_transaction_time %}
Maximum (latest) transaction time for micropayments in this aggregation.
{% enddocs %}

{% docs lp_num_micropayments %}
Number of distinct micropayment ID values for micropayments in this aggregation.
{% enddocs %}

{% docs lp_contains_pre_settlement_refund %}
If "true", this aggregation contains a pre-settlement refund (i.e., contains a micropayment with `charge_type` "refund").
{% enddocs %}

{% docs lp_contains_variable_fare %}
If "true", this aggregation contains at least one micropayment with a variable fare charge type.
{% enddocs %}

{% docs lp_contains_flat_fare %}
If "true", this aggregation contains at least one micropayment with a `flat_fare` charge type.
{% enddocs %}

{% docs lp_contains_pending_charge %}
If "true", this aggregation contains at least one micropayment with a pending charge type.
{% enddocs %}

{% docs lp_contains_adjusted_micropayment %}
If "true", this aggregation contains at least one micropayment that had a micropayment adjustment applied. For example, micropayments that were reduced due to a fare cap being applied will have a "true" in this column.
{% enddocs %}

{% docs lp_settlement_contains_imputed_type %}
Some settlements are missing `settlement_type` (i.e., `DEBIT` vs. `CREDIT` designation).
We impute those missing values on the heuristic that first updates tend to be the debit
and any subsequent updates are credits (refunds).
Rows with "true" in this column indicate that at least one input row had its settlement type imputed.
These rows could potentially (though we believe it is unlikely) be sources of error if the imputation
assumptions were incorrect.
{% enddocs %}

{% docs lp_settlement_contains_refund %}
If `true`, this aggregation settlement included at least one row with settlement_type = `CREDIT`.
{% enddocs %}

{% docs lp_settlement_latest_update_timestamp %}
Most recent `settlement_requested_date_time_utc` value for this aggregation settlement.
If a credit (refund) was issued after the initial debit, this will be the timestamp of the credit.
{% enddocs %}

{% docs lp_net_settled_amount_dollars %}
Net dollar amount of this aggregation settlement; if a refund (credit) has been issued,
that will be reflected. So for example if $20 was debited and then $8 was credited,
the value in this column will be `12` (= 20 - 8).
{% enddocs %}

{% docs lp_settlement_debit_amount %}
Total dollar amount associated with debit settlements in this aggregation.
Numbers in this column are positive because they represent amounts debited (charged) by the participant to the customer (rider);
i.e., these values represent income for the participant (agency).
{% enddocs %}

{% docs lp_settlement_credit_amount %}
Total dollar amount associated with credit (refund) settlements in this aggregation.
Numbers in this column are negative because they represent amounts credited (refunded) by the participant (agency) to the customer (rider);
i.e., these values represent costs for the participant (agency).
{% enddocs %}

---------------- SETTLEMENTS TABLE ----------------

{% docs lp_settlement_id %}
A unique identifier for each settlement.
{% enddocs %}

{% docs lp_aggregation_id %}
Identifies an aggregation of one or more micropayments that can be authorised/settled.
{% enddocs %}

{% docs lp_customer_id %}
Identifies the customer that the micropayment belongs to.
{% enddocs %}

{% docs lp_funding_source_id %}
Identifies the funding source (for example, card) that the micropayment will be charged to. This is always the card that was tapped.

A registered customer can have multiple funding sources linked to it. This field can be used to join to the `customer_funding_source` feed.
{% enddocs %}

{% docs lp_settlement_type %}
Type of settlement that occurred. Possible values are `DEBIT` or `CREDIT`.

If refunding a micropayment that has already been settled, the value will be `CREDIT`.
{% enddocs %}

{% docs lp_transaction_amount %}
The settlement amount.
{% enddocs %}

{% docs lp_retrieval_reference_number %}
Uniquely identifies a card transaction, based on the ISO 8583 standard.

If the acquirer is Elavon, this value will be split between `littlepay_reference_number` and `external_reference_number`.
{% enddocs %}

{% docs lp_littlepay_reference_number %}
Uniquely identifies a card transaction.

If the acquirer is Elavon, then this key will contain the first part of the string from `retrieval_reference_number`.
{% enddocs %}

{% docs lp_external_reference_number %}
Uniquely identifies a card transaction.

If the acquirer is Elavon, then this key will contain the second part of the string from `retrieval_reference_number`.
{% enddocs %}

{% docs lp_settlement_requested_date_time_utc %}
Timestamp of when the settlement request was submitted to the acquirer.
Per October 2023 updates from Littlepay, it may be more appropriate
to interpret this field as a "last updated" value.
{% enddocs %}

{% docs lp_acquirer %}
Identifies the acquirer used to settle the transaction.
{% enddocs %}